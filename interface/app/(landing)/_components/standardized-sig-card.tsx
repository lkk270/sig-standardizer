"use client";
import { Card } from "@/components/ui/card";
import { useTextProcessing } from "@/hooks/use-text-processing";
import Skeleton from "@/components/reusable/skeleton";

interface MedicationEntry {
	medication: string;
	sig_code: string;
	dosage: string;
	frequency: string;
	quantity: string;
	refills: string;
	purpose: string | null;
}

const StandardizedSigCard = () => {
	const { standardizedText, status } = useTextProcessing();
	const isLoading = status === "standardizing" || status === "extracting";

	const formatSigText = (text: string) => {
		if (!text) return null;

		try {
			const medications: MedicationEntry[] = JSON.parse(text);

			return medications.map((med, index) => (
				<div key={index} className="mb-4 bg-primary/20 p-3 rounded-lg">
					<h4 className="font-semibold text-primary mb-1">{med.medication}</h4>
					<div className="text-sm text-muted-foreground space-y-1">
						<p>
							<span className="font-medium">SIG Code:</span> {med.sig_code}
						</p>
						<p>
							<span className="font-medium">Dosage:</span> {med.dosage}
						</p>
						<p>
							<span className="font-medium">Frequency:</span> {med.frequency}
						</p>
						<p>
							<span className="font-medium">Quantity:</span> {med.quantity}
						</p>
						<p>
							<span className="font-medium">Refills:</span> {med.refills}
						</p>
						{med.purpose && (
							<p>
								<span className="font-medium">Purpose:</span> {med.purpose}
							</p>
						)}
					</div>
				</div>
			));
		} catch (error) {
			console.error("Error parsing medication data:", error);
			return null;
		}
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
