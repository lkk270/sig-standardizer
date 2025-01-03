"use client";

import Link from "next/link";
import Image from "next/image";
// import { useMediaQuery } from "usehooks-ts";

import { Poppins } from "next/font/google";

import { cn } from "@/lib/utils";

const font = Poppins({
	subsets: ["latin"],
	weight: ["400", "600"],
});

interface LogoProps {
	textColor?: string;
	showText?: boolean;
	showLgTextSize?: boolean;
}

export const Logo = ({
	textColor,
	showText = true,
	showLgTextSize = true,
}: LogoProps) => {
	// const isMobile = useMediaQuery("(max-width: 500px)");
	const size = "75";
	return (
		<Link
			href="/"
			className={cn(showText ? "sm:w-32" : "")}
			onDragStart={(e) => e.preventDefault()}
		>
			<div className="flex items-center gap-x-2">
				<Image
					className="shrink-0"
					priority={true}
					src="/logo.png"
					height={size}
					width={size}
					alt="Logo"
					draggable={false}
				/>
				{showText && (
					<p
						className={cn(
							"hidden font-semibold text-sm sm:flex gap-x-2",
							showLgTextSize && "sm:text-lg",
							font.className,
							textColor && `text-primary/70`
						)}
					>
						NoSIG
					</p>
				)}
			</div>
		</Link>
	);
};
