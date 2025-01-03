"use client";
import { Card } from "@/components/ui/card";
import { useExtractedText } from "@/hooks/use-extracted-text";
import { useIsLoading } from "@/hooks/use-is-loading";
import Skeleton from "@/components/reusable/skeleton";

const ExtractedTextCard = () => {
	const { extractedText } = useExtractedText();
	const { isLoading } = useIsLoading();
	console.log(isLoading);
	return (
		<Card className="p-4">
			<h3 className="font-bold mb-2">Extracted Text</h3>
			<div className="w-full h-[400px] bg-muted rounded-lg">
				{isLoading ? (
					<div className="space-y-2">
						<Skeleton className="h-4 w-3/4" />
						<Skeleton className="h-4 w-2/4" />
						<Skeleton className="h-4 w-5/6" />
					</div>
				) : (
					extractedText || "No text extracted yet."
				)}
			</div>
		</Card>
	);
};

export default ExtractedTextCard;
