export default function DashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 bg-white dark:bg-gray-900 border rounded-lg">
          <h2 className="text-sm font-medium text-gray-500 mb-1">Portfolio Value</h2>
          <p className="text-2xl font-bold">$10,000.00</p>
        </div>
        <div className="p-6 bg-white dark:bg-gray-900 border rounded-lg">
          <h2 className="text-sm font-medium text-gray-500 mb-1">Day P&L</h2>
          <p className="text-2xl font-bold text-success">+$0.00</p>
        </div>
        <div className="p-6 bg-white dark:bg-gray-900 border rounded-lg">
          <h2 className="text-sm font-medium text-gray-500 mb-1">Active Strategies</h2>
          <p className="text-2xl font-bold">0</p>
        </div>
      </div>
      <p className="mt-8 text-gray-500">
        Connect to the backend API to populate live data.
      </p>
    </div>
  );
}
