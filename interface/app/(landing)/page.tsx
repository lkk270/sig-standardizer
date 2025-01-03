import { FileUploadForm } from "@/components/file-upload/file-upload-form";
import { Navbar } from "@/components/reusable/navbar";
import ExtractedTextCard from "./_components/extracted-text-card";
import StandardizedSigoCard from "./_components/standardized-sigo-card";

export default function Home() {
	return (
		<div className="min-h-screen flex flex-col">
			<Navbar />
			<div className="container mx-auto px-4 py-8 space-y-6 mt-8">
				<div className="max-w-2xl mx-auto">
					<FileUploadForm />
				</div>

				<div className="max-w-6xl mx-auto w-full">
					<div className="grid md:grid-cols-2 gap-4">
						<ExtractedTextCard />
						<StandardizedSigoCard />
					</div>
				</div>
			</div>
		</div>
	);
}
