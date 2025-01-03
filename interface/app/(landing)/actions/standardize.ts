"use server";

type StandardizeResponse = {
	success: boolean;
	text?: string;
	error?: string;
};

export async function standardizeText(
	extractedText: string
): Promise<StandardizeResponse> {
	try {
		if (!process.env.NEXT_PUBLIC_STANDARDIZE_LAMBDA_URL) {
			throw new Error("Standardize Lambda URL is not configured");
		}

		const response = await fetch(
			process.env.NEXT_PUBLIC_STANDARDIZE_LAMBDA_URL,
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					text: extractedText,
				}),
			}
		);

		if (!response.ok) {
			return {
				success: false,
				error: `HTTP error! status: ${response.status}`,
			};
		}

		const data = await response.json();
		console.log(data);

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
