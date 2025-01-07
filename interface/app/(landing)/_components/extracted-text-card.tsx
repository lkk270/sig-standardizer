"use client";
import { Card } from "@/components/ui/card";
import { useTextProcessing } from "@/hooks/use-text-processing";
import Skeleton from "@/components/reusable/skeleton";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState, useEffect } from "react";
import { toast } from "sonner";
import { standardizeText } from "@/app/(landing)/actions/standardize";

const ExtractedTextCard = () => {
	const {
		extractedText,
		status,
		setExtractedText,
		setStatus,
		setStandardizedText,
	} = useTextProcessing();
	const [localText, setLocalText] = useState(extractedText);
	const isLoading = status === "extracting";
	const isProcessing = status === "standardizing" || status === "extracting";

	useEffect(() => {
		setLocalText(extractedText);
	}, [extractedText]);

	const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
		setLocalText(e.target.value);
		setExtractedText(e.target.value);
	};

	const handleProcessText = async () => {
		if (!localText.trim()) {
			toast.error("Please enter some text to process");
			return;
		}

		try {
			setStatus("standardizing");
			const standardizeResult = await standardizeText(localText);

			if (!standardizeResult.success) {
				throw new Error(
					standardizeResult.error || "Failed to standardize text"
				);
			}

			setStandardizedText(standardizeResult.text || "");
			setStatus("completed");
			toast.success("Text processed successfully");
		} catch (error) {
			const errorMessage =
				error instanceof Error ? error.message : "Unknown error occurred";
			setStatus("error");
			toast.error(errorMessage);
		}
	};

	return (
		<Card className="p-4">
			<div className="flex justify-between items-center mb-2">
				<h3 className="font-bold">Extracted Text</h3>
				<Button
					onClick={handleProcessText}
					disabled={isProcessing || !localText}
					variant="outline"
					size="sm"
				>
					Process Text
				</Button>
			</div>
			<div className="w-full h-[400px] bg-muted rounded-lg">
				{isLoading ? (
					<div className="space-y-2 p-4">
						<Skeleton className="h-4 w-3/4" />
						<Skeleton className="h-4 w-2/4" />
						<Skeleton className="h-4 w-5/6" />
					</div>
				) : (
					<Textarea
						value={localText}
						onChange={handleTextChange}
						placeholder="Enter or edit text here..."
						className="h-full resize-none bg-transparent border-none focus-visible:ring-0"
					/>
				)}
			</div>
		</Card>
	);
};

export default ExtractedTextCard;
