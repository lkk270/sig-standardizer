"use client";
import { Card } from "@/components/ui/card";
import { useTextProcessing } from "@/hooks/use-text-processing";
import Skeleton from "@/components/reusable/skeleton";

const StandardizedSigoCard = () => {
	const { standardizedText, status } = useTextProcessing();
	const isLoading = status === "standardizing" || status === "extracting";

	return (
		<Card className="p-4">
			<h3 className="font-bold mb-2">Standardized SIGO</h3>
			<div className="overflow-y-auto p-4 w-full h-[400px] bg-muted rounded-lg">
				{isLoading ? (
					<div className="space-y-2">
						<Skeleton className="h-4 w-3/4" />
						<Skeleton className="h-4 w-2/4" />
						<Skeleton className="h-4 w-5/6" />
					</div>
				) : (
					standardizedText || "No standardized text available."
				)}
			</div>
		</Card>
	);
};

export default StandardizedSigoCard;
