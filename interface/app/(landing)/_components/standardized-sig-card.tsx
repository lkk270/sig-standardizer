"use client";
import { Card } from "@/components/ui/card";
import { useTextProcessing } from "@/hooks/use-text-processing";
import Skeleton from "@/components/reusable/skeleton";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";

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

	const handleDownloadCSV = () => {
		try {
			const data = JSON.parse(standardizedText);
			const medications: MedicationEntry[] = data.medications;

			// Create CSV header
			const headers = [
				"Medication",
				"SIG Code",
				"Dosage",
				"Frequency",
				"Quantity",
				"Refills",
				"Purpose",
			];

			// Convert medications to CSV rows
			const csvRows = [
				headers.join(","),
				...medications.map((med) =>
					[
						`"${med.medication}"`,
						`"${med.sig_code}"`,
						`"${med.dosage}"`,
						`"${med.frequency}"`,
						`"${med.quantity}"`,
						`"${med.refills}"`,
						`"${med.purpose || ""}"`,
					].join(",")
				),
			];

			// Create blob and download
			const csvContent = csvRows.join("\n");
			const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
			const link = document.createElement("a");
			const url = URL.createObjectURL(blob);

			link.setAttribute("href", url);
			link.setAttribute("download", "medications.csv");
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		} catch (error) {
			console.error("Error creating CSV:", error);
		}
	};

	const formatSigText = (text: string) => {
		if (!text) return null;

		try {
			const data = JSON.parse(text);
			const medications: MedicationEntry[] = data.medications;

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
			<div className="flex justify-between items-center mb-2">
				<h3 className="font-bold">Standardized SIG</h3>
				{standardizedText && standardizedText !== "" && (
					<Button
						variant="outline"
						size="sm"
						onClick={handleDownloadCSV}
						className="flex items-center gap-2"
						disabled={!standardizedText || status === "error"}
					>
						<Download className="w-4 h-4" />
						Download CSV
					</Button>
				)}
			</div>
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
					<p className="text-muted-foreground text-center">
						{status === "error"
							? "Unable to standardize text"
							: "No medications or SIG codes found"}
					</p>
				)}
			</div>
		</Card>
	);
};

export default StandardizedSigCard;
