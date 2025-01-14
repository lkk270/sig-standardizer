"use server";

type ExtractTextResponse = {
	success: boolean;
	text?: string;
	error?: string;
	noContent?: boolean;
};

export async function extractText(
	imageData: string
): Promise<ExtractTextResponse> {
	try {
		if (!process.env.NEXT_PUBLIC_LAMBDA_URL) {
			throw new Error("Lambda URL is not configured");
		}

		const response = await fetch(process.env.NEXT_PUBLIC_LAMBDA_URL, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				image: imageData,
			}),
		});

		if (!response.ok) {
			return {
				success: false,
				error: `HTTP error! status: ${response.status}`,
			};
		}

		const data = await response.json();

		if (!data.text || data.text.trim() === "") {
			return {
				success: false,
				noContent: true,
				error: "No text could be extracted from the image",
			};
		}

		return {
			success: true,
			text: data.text,
		};
	} catch (error) {
		console.error("[Server] Error details:", {
			name: error instanceof Error ? error.name : "Unknown",
			message: error instanceof Error ? error.message : String(error),
			stack: error instanceof Error ? error.stack : undefined,
		});

		return {
			success: false,
			error: error instanceof Error ? error.message : "Unknown error occurred",
		};
	}
}
