import { Navbar } from "@/components/reusable/navbar";

export default function Home() {
	return (
		<div className="min-h-screen flex flex-col">
			<Navbar />
			<div className="flex-grow flex items-center justify-center"></div>
		</div>
	);
}
