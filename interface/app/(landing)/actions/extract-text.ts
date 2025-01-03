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
		// Debug logging for server
		console.log("[Server] Starting text extraction");
		console.log(
			"[Server] Lambda URL configured:",
			!!process.env.NEXT_PUBLIC_LAMBDA_URL
		);
		console.log(
			"[Server] Image data received:",
			!!imageData,
			"length:",
			imageData?.length
		);

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
		console.log("[Server] Response received:", {
			status: response.status,
			ok: response.ok,
			headers: Object.fromEntries(response.headers),
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error("[Server] Response error:", {
				status: response.status,
				body: errorText,
			});
			return {
				success: false,
				error: `HTTP error! status: ${response.status}`,
			};
		}

		const data = await response.json();
		console.log("[Server] Response data:", data);

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
