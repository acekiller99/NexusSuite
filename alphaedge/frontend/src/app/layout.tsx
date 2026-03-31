import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AlphaEdge — Stock Trading Bot",
  description: "Automated stock trading platform with real-time data, strategy engine, and portfolio management.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 dark:bg-gray-950">
        {children}
      </body>
    </html>
  );
}
