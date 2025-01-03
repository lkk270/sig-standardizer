"use client";
import { Card } from "@/components/ui/card";
import { useTextProcessing } from "@/hooks/use-text-processing";
import Skeleton from "@/components/reusable/skeleton";

const StandardizedSigCard = () => {
	const { standardizedText, status } = useTextProcessing();
	const isLoading = status === "standardizing" || status === "extracting";

	const formatSigText = (text: string) => {
		if (!text) return null;

		// Split the text into individual medication entries
		return text
			.split("\n")
			.map((line, index) => {
				if (!line.trim()) return null;

				// Find the index of the first colon
				const firstColonIndex = line.indexOf(":");
				if (firstColonIndex === -1) return null;

				const medication = line.substring(0, firstColonIndex);
				const instructions = line.substring(firstColonIndex + 1);

				return (
					<div key={index} className="mb-4 bg-primary/20 p-3 rounded-lg">
						<h4 className="font-semibold text-primary mb-1">
							{medication.trim()}
						</h4>
						<p className="text-sm text-muted-foreground">
							{instructions.trim()}
						</p>
					</div>
				);
			})
			.filter(Boolean); // Remove null entries
	};

	return (
		<Card className="p-4">
			<h3 className="font-bold mb-2">Standardized SIG</h3>
			<div className="overflow-y-auto p-4 w-full h-[400px] bg-muted rounded-lg">
				{isLoading ? (
					<div className="space-y-2">
						<Skeleton className="h-4 w-3/4" />
						<Skeleton className="h-4 w-2/4" />
						<Skeleton className="h-4 w-5/6" />
					</div>
				) : standardizedText ? (
					<div className="space-y-2">{formatSigText(standardizedText)}</div>
				) : (
					<p className="text-muted-foreground">
						No standardized text available.
					</p>
				)}
			</div>
		</Card>
	);
};

export default StandardizedSigCard;
