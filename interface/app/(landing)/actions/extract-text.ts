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
		// Debug logging
		console.log("Lambda URL:", process.env.NEXT_PUBLIC_LAMBDA_URL);
		console.log("Image data length:", imageData?.length);

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

		// Debug response
		console.log("Response status:", response.status);
		console.log("Response headers:", Object.fromEntries(response.headers));

		if (!response.ok) {
			console.error("Response error:", response);
			return {
				success: false,
				error: `HTTP error! status: ${response.status}`,
			};
		}

		const data = await response.json();
		console.log("Response data:", data);

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
		console.error("Error details:", {
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
