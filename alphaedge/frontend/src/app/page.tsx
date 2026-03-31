import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 dark:text-white mb-4">
          AlphaEdge
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
          Automated Stock Trading Bot — Strategies, Backtesting & Real-time Market Data
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
          <div className="p-6 border rounded-lg bg-white dark:bg-gray-900">
            <h2 className="font-semibold text-lg mb-2">Strategy Engine</h2>
            <p className="text-sm text-gray-500">
              Define, backtest and run custom trading strategies
            </p>
          </div>
          <div className="p-6 border rounded-lg bg-white dark:bg-gray-900">
            <h2 className="font-semibold text-lg mb-2">Portfolio Tracker</h2>
            <p className="text-sm text-gray-500">
              Track positions, P&L and cash balance in real time
            </p>
          </div>
          <div className="p-6 border rounded-lg bg-white dark:bg-gray-900">
            <h2 className="font-semibold text-lg mb-2">Market Data</h2>
            <p className="text-sm text-gray-500">
              Live quotes, historical charts and technical indicators
            </p>
          </div>
          <div className="p-6 border rounded-lg bg-white dark:bg-gray-900">
            <h2 className="font-semibold text-lg mb-2">Paper Trading</h2>
            <p className="text-sm text-gray-500">
              Risk-free practice trading before going live
            </p>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <Link
            href="/dashboard"
            className="px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition"
          >
            Dashboard
          </Link>
          <a
            href="/docs"
            className="px-6 py-3 border border-gray-300 rounded-lg font-medium hover:bg-gray-100 dark:hover:bg-gray-800 transition"
          >
            API Docs
          </a>
        </div>
      </div>
    </main>
  );
}
