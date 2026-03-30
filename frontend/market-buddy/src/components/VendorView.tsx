import {
  ArrowLeft,
  Trash2,
  Save,
  Search,
  Moon,
  Sun,
  Download,
  Printer,
  PackageOpen,
  LogOut,
} from "lucide-react";
import {
  PRODUCTS,
  getLatestPrice,
  getPrices,
  upsertPrice,
  deletePrice,
  getTrendDirection,
  getSales,
  addSale,
  deleteSale,
  getDailyRevenue,
  getDailyProfit,
  getProductStock,
  setProductStock,
  exportSalesCSV,
  getProductImages,
  saveProductImage,
  type SubMarket,
  type PriceEntry,
  type SaleEntry,
} from "@/lib/data";
import PriceChart from "./PriceChart";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useTheme } from "next-themes";
import QRCode from "react-qr-code";

interface VendorViewProps {
  market: SubMarket;
  onBack: () => void;
}

const CATEGORIES = ["All", "Fruit", "Vegetable", "Grain", "Spice"] as const;

/** Trigger a file download in the browser */
function downloadFile(filename: string, content: string, mime = "text/csv") {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function VendorView({ market, onBack }: VendorViewProps) {
  const [category, setCategory] = useState<string>("All");
  const [search, setSearch] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<string | null>(null);
  const [priceInput, setPriceInput] = useState("");
  const [saleQuantity, setSaleQuantity] = useState("");
  const [salePrice, setSalePrice] = useState("");
  const [saleCost, setSaleCost] = useState(""); // NEW: cost per unit input
  const [salesSearch, setSalesSearch] = useState("");
  const [salesPage, setSalesPage] = useState(1);
  const [selectedSales, setSelectedSales] = useState<Set<string>>(new Set());
  const [productImages, setProductImages] = useState<Record<string, string>>({});
  const [selectedTab, setSelectedTab] = useState<"prices" | "sales" | "analytics" | "inventory">(
    "prices"
  );
  const [sales, setSales] = useState<SaleEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [receiptSale, setReceiptSale] = useState<SaleEntry | null>(null);
  const [refresh, setRefresh] = useState(0);

  // Stock editing state: { [productId]: string } for in-progress edits
  const [stockEdits, setStockEdits] = useState<Record<string, string>>({});
  // Stock values cached in component state (loaded from localStorage)
  const [stockMap, setStockMap] = useState<Record<string, number>>({});

  const { theme, setTheme } = useTheme();
  const printRef = useRef<HTMLDivElement>(null);

  const today = new Date().toISOString().split("T")[0];

  const handleLogout = () => {
    sessionStorage.removeItem("authenticated");
    localStorage.removeItem("access_token");
    window.location.reload();
  };

  // ── Load stock from localStorage for all products in this market ──────────
  useEffect(() => {
    const map: Record<string, number> = {};
    for (const p of PRODUCTS) {
      map[p.id] = getProductStock(p.id, market.id);
    }
    setStockMap(map);
  }, [market.id, refresh]);

  const filtered = useMemo(
    () =>
      PRODUCTS.filter(
        (p) =>
          (category === "All" || p.category === category) &&
          p.name.toLowerCase().includes(search.toLowerCase())
      ),
    [category, search]
  );

  useEffect(() => {
    setProductImages(getProductImages());
    setTimeout(() => setIsLoading(false), 500);
  }, [refresh]);

  useEffect(() => {
    const marketSales = getSales().filter((s) => s.subMarketId === market.id);
    setSales(marketSales);
  }, [market.id, isLoading, refresh]);

  const refreshSales = () => {
    const marketSales = getSales().filter((s) => s.subMarketId === market.id);
    setSales(marketSales);
  };

  // ── Prices ────────────────────────────────────────────────────────────────
  const handleSavePrice = () => {
    if (!selectedProduct || !priceInput) return;
    const val = parseFloat(priceInput);
    if (isNaN(val) || val <= 0) return;
    upsertPrice(selectedProduct, market.id, val, today);
    setPriceInput("");
    setRefresh((r) => r + 1);
  };

  const handleDeletePrice = (priceId: string) => {
    deletePrice(priceId);
    setRefresh((r) => r + 1);
  };

  // ── Sales ─────────────────────────────────────────────────────────────────
  const handleRecordSale = () => {
    if (!selectedProduct) return;
    const quantity = Number(saleQuantity);
    if (Number.isNaN(quantity) || quantity <= 0) return;

    let unitPrice = Number(salePrice);
    if (Number.isNaN(unitPrice) || unitPrice <= 0) {
      const latest = getLatestPrice(selectedProduct, market.id);
      unitPrice = latest?.price ?? 0;
    }
    if (unitPrice <= 0) return;

    const costPerUnit = saleCost !== "" ? Number(saleCost) : undefined;
    const sale = addSale(selectedProduct, market.id, quantity, unitPrice, today, costPerUnit);

    // Decrease stock
    const currentStock = stockMap[selectedProduct] ?? 100;
    const newStock = Math.max(0, currentStock - quantity);
    setProductStock(selectedProduct, market.id, newStock);

    setSaleQuantity("");
    setSalePrice("");
    setSaleCost("");
    setSales((prev) => [sale, ...prev]);
    setStockMap((prev) => ({ ...prev, [selectedProduct]: newStock }));
    setReceiptSale(sale);
    setTimeout(() => window.print(), 200);
  };

  const handleDeleteSale = (saleId: string) => {
    deleteSale(saleId);
    refreshSales();
  };

  const handleDeleteSelectedSales = () => {
    Array.from(selectedSales).forEach(id => deleteSale(id));
    setSelectedSales(new Set());
    refreshSales();
  };

  const toggleSaleSelection = (saleId: string) => {
    setSelectedSales(prev => {
      const next = new Set(prev);
      if (next.has(saleId)) next.delete(saleId);
      else next.add(saleId);
      return next;
    });
  };

  const toggleSelectAllSales = (ids: string[]) => {
    if (selectedSales.size === ids.length && ids.length > 0) {
      setSelectedSales(new Set());
    } else {
      setSelectedSales(new Set(ids));
    }
  };

  // ── CSV Export ────────────────────────────────────────────────────────────
  const handleExportCSV = () => {
    const csv = exportSalesCSV(market.id);
    const marketSlug = market.name.replace(/\s+/g, "_").toLowerCase();
    downloadFile(`${marketSlug}_sales_${today}.csv`, csv);
  };

  // ── Stock management ──────────────────────────────────────────────────────
  const handleSaveStock = (productId: string) => {
    const val = Number(stockEdits[productId]);
    if (isNaN(val) || val < 0) return;
    setProductStock(productId, market.id, val);
    setStockMap((prev) => ({ ...prev, [productId]: val }));
    setStockEdits((prev) => {
      const next = { ...prev };
      delete next[productId];
      return next;
    });
  };

  // ── Derived data ──────────────────────────────────────────────────────────
  const handleImageUpload = (productId: string, e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      const base64 = event.target?.result as string;
      saveProductImage(productId, base64);
      setProductImages((prev) => ({ ...prev, [productId]: base64 }));
    };
    reader.readAsDataURL(file);
  };
  const todayPrices = getPrices().filter(
    (p) => p.subMarketId === market.id && p.date === today
  );

  const salesFiltered = useMemo(() => {
    return sales.filter((sale) => {
      const product = PRODUCTS.find((p) => p.id === sale.productId);
      return (
        !salesSearch ||
        product?.name.toLowerCase().includes(salesSearch.toLowerCase()) ||
        sale.date.includes(salesSearch)
      );
    });
  }, [sales, salesSearch]);

  const salesPerPage = 6;
  const salesTotalPages = Math.max(1, Math.ceil(salesFiltered.length / salesPerPage));
  const salesPageItems = salesFiltered.slice(
    (salesPage - 1) * salesPerPage,
    salesPage * salesPerPage
  );

  const revenueData = useMemo(() => getDailyRevenue(market.id, 7), [sales]);
  const profitData = useMemo(() => getDailyProfit(market.id, 7), [sales]);

  const weekRevenue = revenueData.reduce((sum, d) => sum + d.revenue, 0);
  const weekProfit = profitData.reduce((sum, d) => sum + d.profit, 0);
  const weekCost = profitData.reduce((sum, d) => sum + d.cost, 0);

  const toggleTheme = () => setTheme(theme === "dark" ? "light" : "dark");

  // ── QR payload for receipt ────────────────────────────────────────────────
  const receiptQRPayload = receiptSale
    ? JSON.stringify({
        market: market.name,
        product: PRODUCTS.find((p) => p.id === receiptSale.productId)?.name,
        qty: receiptSale.quantity,
        rate: receiptSale.pricePerUnit,
        total: receiptSale.total,
        date: receiptSale.date,
        id: receiptSale.id,
      })
    : "";

  return (
    <div className="min-h-screen px-4 py-6">
      <div className="mx-auto max-w-6xl">
        {/* ── Header ────────────────────────────────────────────────── */}
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="h-5 w-5" /> Back
          </button>

          <div className="flex flex-wrap gap-2">
            {(["prices", "sales", "analytics", "inventory"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setSelectedTab(tab)}
                className={`rounded-lg px-3 py-2 text-sm font-medium capitalize ${
                  selectedTab === tab
                    ? "bg-vendor text-vendor-foreground"
                    : "border border-border bg-card text-foreground"
                }`}
              >
                {tab === "inventory" ? "📦 Inventory" : tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          <div className="flex gap-2">
            <button
              onClick={toggleTheme}
              className="rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground hover:bg-accent"
            >
              {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </button>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 rounded-lg border border-destructive bg-destructive/10 px-3 py-2 text-sm text-destructive hover:bg-destructive hover:text-destructive-foreground transition-colors"
            >
              <LogOut className="h-4 w-4" /> Logout
            </button>
          </div>
        </div>

        <h2 className="text-2xl font-bold text-foreground">{market.name}</h2>
        <p className="mb-6 text-sm text-muted-foreground">{market.area}, Mumbai — Vendor View</p>

        {sessionStorage.getItem("authenticated") === "guest" && (
          <div className="mb-6 rounded-lg bg-blue-500/10 p-4 border border-blue-500/20 text-blue-600 dark:text-blue-400">
            <p className="flex items-center gap-2 text-sm font-medium">
              You are currently logged in as a Guest. Showing dummy data. Real changes will not be saved.
            </p>
          </div>
        )}

        {/* ── Skeleton loader ───────────────────────────────────────── */}
        {isLoading ? (
          <div className="space-y-3">
            {[...Array(5)].map((_, idx) => (
              <div key={idx} className="h-16 animate-pulse rounded-lg bg-muted" />
            ))}
          </div>
        ) : (
          <>
            {/* ════════════════════════════════ PRICES TAB ══════════════ */}
            {selectedTab === "prices" && (
              <div className="grid gap-6 lg:grid-cols-3">
                <div className="lg:col-span-2">
                  <h3 className="mb-3 text-lg font-bold text-foreground">Update Price</h3>

                  <p className="mb-2 text-sm font-medium text-foreground">Filter by Category</p>
                  <div className="mb-4 flex flex-wrap gap-2">
                    {CATEGORIES.map((c) => (
                      <button
                        key={c}
                        onClick={() => setCategory(c)}
                        className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                          category === c
                            ? "bg-vendor text-vendor-foreground"
                            : "border border-border bg-card text-foreground hover:bg-accent"
                        }`}
                      >
                        {c}
                      </button>
                    ))}
                  </div>

                  <p className="mb-2 text-sm font-medium text-foreground">Select Product</p>
                  <div className="relative mb-4">
                    <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                    <input
                      type="text"
                      placeholder="Search products..."
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      className="w-full rounded-lg border border-border bg-card py-2.5 pl-9 pr-4 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                  </div>

                  <div className="mb-4 grid max-h-72 gap-2 overflow-y-auto sm:grid-cols-2">
                    {filtered.map((product) => {
                      const latest = getLatestPrice(product.id, market.id);
                      const isActive = selectedProduct === product.id;
                      const stock = stockMap[product.id] ?? 100;
                      return (
                        <button
                          key={product.id}
                          onClick={() => {
                            setSelectedProduct(product.id);
                            setPriceInput(latest?.price.toString() ?? "");
                          }}
                          className={`rounded-lg border p-3 text-left transition-colors ${
                            isActive
                              ? "border-vendor bg-vendor/5"
                              : "border-border bg-card hover:bg-accent"
                          }`}
                        >
                          <p className="font-medium text-foreground">{product.name}</p>
                          <p className="text-xs text-muted-foreground">
                            {product.category} • Stock: {stock}
                            {latest ? ` • ₹${latest.price}` : ""}
                          </p>
                        </button>
                      );
                    })}
                  </div>

                  {selectedProduct && (
                    <div className="rounded-xl border border-border bg-card p-4">
                      <p className="mb-1 text-sm font-medium text-foreground">
                        Set price for {PRODUCTS.find((p) => p.id === selectedProduct)?.name}
                      </p>
                      <p className="mb-3 text-xs text-muted-foreground">7-Day Trend</p>
                      <PriceChart productId={selectedProduct} subMarketId={market.id} height={120} />
                      <div className="mt-3 flex flex-col gap-2 sm:flex-row">
                        <input
                          type="number"
                          placeholder="₹ Price"
                          value={priceInput}
                          onChange={(e) => setPriceInput(e.target.value)}
                          className="flex-1 rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                        />
                        <button
                          onClick={handleSavePrice}
                          className="flex items-center justify-center gap-1 rounded-lg bg-vendor px-4 py-2 text-sm font-medium text-vendor-foreground hover:opacity-90"
                        >
                          <Save className="h-4 w-4" /> Save
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                <div>
                  <h3 className="mb-3 text-lg font-bold text-foreground">Market Today</h3>
                  <div className="space-y-3">
                    {todayPrices.length === 0 && (
                      <p className="text-sm text-muted-foreground">No prices updated today.</p>
                    )}
                    {todayPrices.map((entry) => {
                      const product = PRODUCTS.find((p) => p.id === entry.productId);
                      if (!product) return null;
                      const trend = getTrendDirection(entry.productId, market.id);
                      return (
                        <div
                          key={entry.id}
                          className="flex items-center justify-between rounded-lg border border-border border-l-4 border-l-vendor bg-card p-3"
                        >
                          <div>
                            <p className="font-medium text-foreground">{product.name}</p>
                            <p className="text-lg font-bold text-vendor">₹{entry.price}</p>
                            <p className="text-xs text-muted-foreground">{product.unit}</p>
                          </div>
                          <div className="flex flex-col items-end gap-2">
                            {trend === "up" && <span className="text-xs text-chart-down">↗</span>}
                            {trend === "down" && <span className="text-xs text-chart-up">↘</span>}
                            <button
                              onClick={() => handleDeletePrice(entry.id)}
                              className="rounded p-1 text-muted-foreground hover:bg-destructive/10 hover:text-destructive"
                            >
                              <Trash2 className="h-4 w-4" />
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* ════════════════════════════════ SALES TAB ═══════════════ */}
            {selectedTab === "sales" && (
              <div className="grid gap-6 lg:grid-cols-3">
                {/* Record Sale form */}
                <div className="lg:col-span-2">
                  <h3 className="mb-3 text-lg font-bold text-foreground">Record Sale</h3>
                  <div className="space-y-3 rounded-xl border border-border bg-card p-4">
                    <p className="text-sm text-muted-foreground">Product</p>
                    <select
                      className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                      value={selectedProduct ?? ""}
                      onChange={(e) => {
                        const id = e.target.value;
                        setSelectedProduct(id || null);
                        const latest = id ? getLatestPrice(id, market.id) : null;
                        setSalePrice(latest?.price.toString() ?? "");
                      }}
                    >
                      <option value="">Select product</option>
                      {PRODUCTS.map((product) => {
                        const stock = stockMap[product.id] ?? 100;
                        return (
                          <option key={product.id} value={product.id}>
                            {product.name} (stock: {stock}) {stock < 5 ? '⚠️ LOW STOCK' : ''}
                          </option>
                        );
                      })}
                    </select>

                    <div className="grid gap-2 sm:grid-cols-3">
                      <input
                        type="number"
                        min={1}
                        step={1}
                        placeholder="Quantity"
                        value={saleQuantity}
                        onChange={(e) => setSaleQuantity(e.target.value)}
                        className="rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                      />
                      <input
                        type="number"
                        min={0}
                        step="0.01"
                        placeholder="Sale price / unit"
                        value={salePrice}
                        onChange={(e) => setSalePrice(e.target.value)}
                        className="rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                      />
                      <input
                        type="number"
                        min={0}
                        step="0.01"
                        placeholder="Cost / unit (optional)"
                        value={saleCost}
                        onChange={(e) => setSaleCost(e.target.value)}
                        className="rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                      />
                    </div>

                    {selectedProduct && salePrice && saleQuantity && (
                      <div className="rounded-lg bg-muted px-3 py-2 text-sm text-muted-foreground">
                        Revenue:{" "}
                        <strong>₹{(Number(salePrice) * Number(saleQuantity)).toFixed(2)}</strong>
                        {saleCost && (
                          <>
                            {" "}
                            · Profit:{" "}
                            <strong className="text-green-500">
                              ₹
                              {(
                                (Number(salePrice) - Number(saleCost)) *
                                Number(saleQuantity)
                              ).toFixed(2)}
                            </strong>
                          </>
                        )}
                      </div>
                    )}

                    <button
                      onClick={handleRecordSale}
                      className="inline-flex items-center gap-2 rounded-lg bg-vendor px-4 py-2 text-sm font-medium text-vendor-foreground hover:opacity-90"
                    >
                      <Save className="h-4 w-4" /> Record Sale
                    </button>
                  </div>
                </div>

                {/* Quick Stats */}
                <div className="lg:col-span-1">
                  <h3 className="mb-3 text-lg font-bold text-foreground">Quick Stats</h3>
                  <div className="space-y-3 rounded-xl border border-border bg-card p-4">
                    <div>
                      <p className="text-xs text-muted-foreground">Total Transactions</p>
                      <p className="text-2xl font-bold text-vendor">{sales.length}</p>
                    </div>
                    <div>
                      <p className="text-xs text-muted-foreground">7-Day Revenue</p>
                      <p className="text-2xl font-bold text-primary">₹{weekRevenue.toFixed(2)}</p>
                    </div>
                    {weekCost > 0 && (
                      <div>
                        <p className="text-xs text-muted-foreground">7-Day Profit</p>
                        <p className="text-2xl font-bold text-green-500">
                          ₹{weekProfit.toFixed(2)}
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Transaction History */}
                <div className="lg:col-span-3">
                  <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
                    <h3 className="text-lg font-bold text-foreground">Transaction History</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedSales.size > 0 && (
                        <button
                          onClick={handleDeleteSelectedSales}
                          className="inline-flex items-center gap-2 rounded-lg bg-destructive px-3 py-2 text-sm font-medium text-destructive-foreground hover:opacity-90"
                        >
                          <Trash2 className="h-4 w-4" /> Delete Selected ({selectedSales.size})
                        </button>
                      )}
                      <button
                        onClick={handleExportCSV}
                        className="inline-flex items-center gap-2 rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground hover:bg-accent"
                      >
                        <Download className="h-4 w-4" /> Export CSV
                      </button>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center justify-between gap-2 pb-3">
                    <input
                      type="text"
                      placeholder="Search transaction..."
                      value={salesSearch}
                      onChange={(e) => {
                        setSalesSearch(e.target.value);
                        setSalesPage(1);
                      }}
                      className="w-full max-w-sm rounded-lg border border-border bg-card px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                  </div>

                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                      <thead>
                        <tr className="border-b border-border text-muted-foreground">
                          <th className="px-2 py-2">
                            <input
                              type="checkbox"
                              checked={salesPageItems.length > 0 && selectedSales.size === salesPageItems.length}
                              onChange={() => toggleSelectAllSales(salesPageItems.map(s => s.id))}
                              className="rounded border-border accent-vendor"
                            />
                          </th>
                          <th className="px-2 py-2">Date</th>
                          <th className="px-2 py-2">Product</th>
                          <th className="px-2 py-2">Qty</th>
                          <th className="px-2 py-2">Unit</th>
                          <th className="px-2 py-2">Revenue</th>
                          <th className="px-2 py-2">Profit</th>
                          <th className="px-2 py-2">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {salesPageItems.length === 0 ? (
                          <tr>
                            <td className="p-2" colSpan={8}>
                              <p className="text-sm text-muted-foreground">No sales found.</p>
                            </td>
                          </tr>
                        ) : (
                          salesPageItems.map((sale) => {
                            const product = PRODUCTS.find((p) => p.id === sale.productId);
                            return (
                              <tr key={sale.id} className="border-b border-border">
                                <td className="px-2 py-2">
                                  <input
                                    type="checkbox"
                                    checked={selectedSales.has(sale.id)}
                                    onChange={() => toggleSaleSelection(sale.id)}
                                    className="rounded border-border accent-vendor"
                                  />
                                </td>
                                <td className="px-2 py-2 text-xs">{sale.date}</td>
                                <td className="px-2 py-2">{product?.name ?? "Unknown"}</td>
                                <td className="px-2 py-2">{sale.quantity}</td>
                                <td className="px-2 py-2 text-xs">{product?.unit ?? "unit"}</td>
                                <td className="px-2 py-2">₹{sale.total.toFixed(2)}</td>
                                <td className="px-2 py-2">
                                  {sale.profit !== undefined ? (
                                    <span
                                      className={
                                        sale.profit >= 0 ? "text-green-500" : "text-destructive"
                                      }
                                    >
                                      ₹{sale.profit.toFixed(2)}
                                    </span>
                                  ) : (
                                    <span className="text-muted-foreground text-xs">—</span>
                                  )}
                                </td>
                                <td className="px-2 py-2">
                                  <button
                                    onClick={() => {
                                      setReceiptSale(sale);
                                      setTimeout(() => window.print(), 200);
                                    }}
                                    className="mr-2 inline-flex items-center gap-1 rounded-lg border border-border px-2 py-1 text-xs hover:bg-accent"
                                  >
                                    <Printer className="h-3 w-3" /> Receipt
                                  </button>
                                  <button
                                    onClick={() => handleDeleteSale(sale.id)}
                                    className="inline-flex items-center gap-1 rounded-lg border border-destructive px-2 py-1 text-xs text-destructive hover:bg-destructive/10"
                                  >
                                    <Trash2 className="h-3 w-3" /> Delete
                                  </button>
                                </td>
                              </tr>
                            );
                          })
                        )}
                      </tbody>
                    </table>
                  </div>

                  <div className="mt-2 flex gap-2 text-sm">
                    <button
                      onClick={() => setSalesPage((p) => Math.max(1, p - 1))}
                      disabled={salesPage <= 1}
                      className="rounded-lg border border-border px-3 py-1 text-muted-foreground disabled:opacity-50"
                    >
                      Prev
                    </button>
                    <span className="px-2 py-1">
                      Page {salesPage} of {salesTotalPages}
                    </span>
                    <button
                      onClick={() => setSalesPage((p) => Math.min(salesTotalPages, p + 1))}
                      disabled={salesPage >= salesTotalPages}
                      className="rounded-lg border border-border px-3 py-1 text-muted-foreground disabled:opacity-50"
                    >
                      Next
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* ════════════════════════════ ANALYTICS TAB ═══════════════ */}
            {selectedTab === "analytics" && (
              <div className="space-y-6">
                {/* Summary cards */}
                <div className="grid gap-4 sm:grid-cols-3">
                  {[
                    { label: "7-Day Revenue", value: `₹${weekRevenue.toFixed(2)}`, color: "text-primary" },
                    { label: "7-Day Cost", value: weekCost > 0 ? `₹${weekCost.toFixed(2)}` : "—", color: "text-destructive" },
                    {
                      label: "7-Day Profit",
                      value: weekCost > 0 ? `₹${weekProfit.toFixed(2)}` : "—",
                      color: weekProfit >= 0 ? "text-green-500" : "text-destructive",
                    },
                  ].map((card) => (
                    <div
                      key={card.label}
                      className="rounded-xl border border-border bg-card p-4 shadow-sm"
                    >
                      <p className="text-xs text-muted-foreground">{card.label}</p>
                      <p className={`text-2xl font-bold ${card.color}`}>{card.value}</p>
                    </div>
                  ))}
                </div>

                {/* Profit vs Revenue + Cost grouped bar chart */}
                <div className="rounded-xl border border-border bg-card p-4">
                  <h3 className="mb-2 text-lg font-bold text-foreground">
                    Weekly Profit vs Revenue vs Cost
                  </h3>
                  <p className="mb-4 text-xs text-muted-foreground">
                    Cost columns only appear when cost/unit is recorded against a sale.
                  </p>
                  <div className="h-72">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={profitData} barCategoryGap="25%">
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                        <YAxis tick={{ fontSize: 10 }} />
                        <Tooltip formatter={(value: number) => `₹${value.toFixed(2)}`} />
                        <Legend />
                        <Bar dataKey="revenue" name="Revenue" fill="#6366f1" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="cost" name="Cost" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="profit" name="Profit" fill="#22c55e" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Revenue trend (area) */}
                <div className="rounded-xl border border-border bg-card p-4">
                  <h3 className="mb-2 text-lg font-bold text-foreground">Revenue Trend</h3>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={revenueData}>
                        <defs>
                          <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#6366f1" stopOpacity={0.1} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="date" tick={{ fontSize: 10 }} />
                        <YAxis tick={{ fontSize: 10 }} />
                        <Tooltip formatter={(value: number) => `₹${value.toFixed(2)}`} />
                        <Area
                          type="monotone"
                          dataKey="revenue"
                          stroke="#6366f1"
                          fillOpacity={1}
                          fill="url(#colorRev)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            )}

            {/* ════════════════════════════ INVENTORY TAB ═══════════════ */}
            {selectedTab === "inventory" && (
              <div>
                <div className="mb-4 flex items-center gap-2">
                  <PackageOpen className="h-5 w-5 text-vendor" />
                  <h3 className="text-lg font-bold text-foreground">Product Stock Settings</h3>
                </div>
                <p className="mb-4 text-sm text-muted-foreground">
                  Set the current stock level for each product at{" "}
                  <strong>{market.name}</strong>. Stock is automatically decremented when a sale is
                  recorded.
                </p>

                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                  {PRODUCTS.map((product) => {
                    const stock = stockMap[product.id] ?? 100;
                    const isEditing = stockEdits[product.id] !== undefined;
                    return (
                      <div
                        key={product.id}
                        className="rounded-xl border border-border bg-card p-4 shadow-sm"
                      >
                        <div className="mb-2 flex items-center justify-between">
                          <p className="font-medium text-foreground">{product.name}</p>
                          <span className="rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
                            {product.category}
                          </span>
                        </div>
                        {productImages[product.id] && (
                          <div className="mb-3 h-24 w-full overflow-hidden rounded-lg bg-muted flex items-center justify-center">
                            <img src={productImages[product.id]} alt={product.name} className="h-full w-full object-cover" />
                          </div>
                        )}
                        <p className="mb-3 text-sm text-muted-foreground">
                          Current stock:{" "}
                          <strong
                            className={
                              stock < 5
                                ? "text-red-500 font-extrabold"
                                : stock <= 10
                                ? "text-destructive"
                                : stock <= 30
                                ? "text-yellow-500"
                                : "text-green-500"
                            }
                          >
                            {stock} {product.unit}
                          </strong>
                        </p>

                        <div className="mb-3">
                          <label className="text-xs text-muted-foreground block mb-1 font-medium">Product Image</label>
                          <input type="file" accept="image/*" onChange={(e) => handleImageUpload(product.id, e)} className="text-xs file:mr-2 file:cursor-pointer file:rounded-lg file:border-0 file:bg-vendor/10 file:px-2 file:py-1 file:text-xs file:text-vendor hover:file:bg-vendor/20" />
                        </div>

                        {isEditing ? (
                          <div className="flex gap-2">
                            <input
                              type="number"
                              min={0}
                              value={stockEdits[product.id]}
                              onChange={(e) =>
                                setStockEdits((prev) => ({
                                  ...prev,
                                  [product.id]: e.target.value,
                                }))
                              }
                              className="flex-1 rounded-lg border border-border bg-background px-3 py-1.5 text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                            />
                            <button
                              onClick={() => handleSaveStock(product.id)}
                              className="rounded-lg bg-vendor px-3 py-1.5 text-sm font-medium text-vendor-foreground hover:opacity-90"
                            >
                              <Save className="h-4 w-4" />
                            </button>
                            <button
                              onClick={() =>
                                setStockEdits((prev) => {
                                  const next = { ...prev };
                                  delete next[product.id];
                                  return next;
                                })
                              }
                              className="rounded-lg border border-border px-3 py-1.5 text-sm text-muted-foreground hover:bg-accent"
                            >
                              ✕
                            </button>
                          </div>
                        ) : (
                          <button
                            onClick={() =>
                              setStockEdits((prev) => ({
                                ...prev,
                                [product.id]: String(stock),
                              }))
                            }
                            className="w-full rounded-lg border border-border bg-muted px-3 py-1.5 text-sm text-foreground hover:bg-accent"
                          >
                            ✎ Edit Stock
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* ════════════════════════ PRINT RECEIPT ═══════════════════ */}
            {receiptSale && (
              <aside
                ref={printRef}
                className="print:flex print:items-center print:justify-center hidden fixed inset-0 z-50 overflow-auto bg-white p-8"
              >
                <div className="mx-auto w-full max-w-sm border border-gray-200 p-6">
                  <h3 className="mb-1 text-center text-xl font-bold tracking-tight">
                    🧾 Sale Receipt
                  </h3>
                  <p className="mb-4 text-center text-xs text-gray-400">Market Buddy</p>
                  <hr className="mb-4" />

                  <table className="mb-4 w-full text-sm">
                    <tbody>
                      {[
                        ["Market", market.name],
                        ["Date", receiptSale.date],
                        [
                          "Product",
                          PRODUCTS.find((p) => p.id === receiptSale.productId)?.name ?? "—",
                        ],
                        ["Quantity", `${receiptSale.quantity} ${PRODUCTS.find((p) => p.id === receiptSale.productId)?.unit ?? "unit"}`],
                        ["Rate", `₹${receiptSale.pricePerUnit.toFixed(2)}`],
                        ...(receiptSale.costPerUnit !== undefined
                          ? [["Cost/Unit", `₹${receiptSale.costPerUnit.toFixed(2)}`]]
                          : []),
                        ["Total", `₹${receiptSale.total.toFixed(2)}`],
                        ...(receiptSale.profit !== undefined
                          ? [["Profit", `₹${receiptSale.profit.toFixed(2)}`]]
                          : []),
                      ].map(([label, val]) => (
                        <tr key={label} className="border-b border-gray-100">
                          <td className="py-1.5 pr-4 font-medium text-gray-600">{label}</td>
                          <td className="py-1.5 text-gray-900">{val}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  {/* QR Code */}
                  <div className="flex flex-col items-center gap-2 pt-2">
                    <QRCode value={receiptQRPayload} size={120} />
                    <p className="text-xs text-gray-400">Scan to verify sale details</p>
                  </div>

                  <hr className="mt-4" />
                  <p className="mt-2 text-center text-xs text-gray-400">
                    Receipt ID: {receiptSale.id.slice(-10)}
                  </p>
                </div>
              </aside>
            )}
          </>
        )}
      </div>
    </div>
  );
}
