"use server";

type ExtractTextResponse = {
	success: boolean;
	text?: string;
	error?: string;
};

export async function extractText(
	imageData: string
): Promise<ExtractTextResponse> {
	try {
		const response = await fetch(process.env.NEXT_PUBLIC_LAMBDA_URL!, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				image: imageData,
			}),
		});

		if (!response.ok) {
			console.log(response);
			return {
				success: false,
				error: `HTTP error! status: ${response.status}`,
			};
		}

		const data = await response.json();

		if (data.status === "error") {
			return {
				success: false,
				error: data.error || "Unknown error occurred",
			};
		}

		return {
			success: true,
			text: data.text,
		};
	} catch (error) {
		console.error("Error:", error);
		return {
			success: false,
			error: error instanceof Error ? error.message : "Unknown error occurred",
		};
	}
}
