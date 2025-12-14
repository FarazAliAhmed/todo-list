import Header from "@/components/Header";
import ToastContainer from "@/components/ToastContainer";
import { ToastProvider } from "@/lib/toast-context";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Todo App - Phase II",
  description: "Full-stack todo application with authentication",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <ToastProvider>
          <Header />
          {children}
          <ToastContainer />
        </ToastProvider>
      </body>
    </html>
  );
}
