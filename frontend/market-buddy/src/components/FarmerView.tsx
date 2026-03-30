import { ArrowLeft, TrendingUp, TrendingDown, Minus, Lightbulb } from "lucide-react";
import { PRODUCTS, getLatestPrice, getTrendDirection, getNegotiationInsight, type SubMarket } from "@/lib/data";
import PriceChart from "./PriceChart";
import { useState } from "react";

interface FarmerViewProps {
  market: SubMarket;
  onBack: () => void;
}

const CATEGORIES = ["All", "Fruit", "Vegetable", "Grain", "Spice"] as const;

export default function FarmerView({ market, onBack }: FarmerViewProps) {
  const [category, setCategory] = useState<string>("All");
  const [selected, setSelected] = useState<string | null>(null);

  // Profit estimator state
  const [estimateQuantity, setEstimateQuantity] = useState<string>("");
  const [costPerUnit, setCostPerUnit] = useState<string>("");
  const [sellPrice, setSellPrice] = useState<string>("");

  const filtered = PRODUCTS.filter((p) => category === "All" || p.category === category);

  const TrendIcon = ({ productId }: { productId: string }) => {
    const t = getTrendDirection(productId, market.id);
    if (t === "up") return <TrendingUp className="h-4 w-4 text-chart-down" />;
    if (t === "down") return <TrendingDown className="h-4 w-4 text-chart-up" />;
    return <Minus className="h-4 w-4 text-muted-foreground" />;
  };

  return (
    <div className="min-h-screen px-4 py-6">
      <div className="mx-auto max-w-4xl">
        <button onClick={onBack} className="mb-4 flex items-center gap-2 text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h2 className="text-2xl font-bold text-foreground">{market.name}</h2>
        <p className="mb-6 text-sm text-muted-foreground">{market.area}, Mumbai — Farmer View</p>

        <div className="mb-6 flex flex-wrap gap-2">
          {CATEGORIES.map((c) => (
            <button
              key={c}
              onClick={() => setCategory(c)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                category === c
                  ? "bg-primary text-primary-foreground"
                  : "border border-border bg-card text-foreground hover:bg-accent"
              }`}
            >
              {c}
            </button>
          ))}
        </div>

        {/* Profit Estimator Section */}
        {selected && (
          <div className="mb-8 rounded-xl border border-border bg-card p-4">
            <h3 className="mb-4 text-lg font-semibold text-foreground flex items-center gap-2">
              <Lightbulb className="h-5 w-5 text-primary" /> Profit Estimator & Negotiation
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Enter your costs and target sell price for the selected product to estimate profit margins before negotiating.
            </p>
            <div className="grid gap-4 sm:grid-cols-3">
              <div>
                <label className="mb-1 flex text-sm font-medium text-muted-foreground">Est. Quantity</label>
                <input
                  type="number"
                  min="0"
                  value={estimateQuantity}
                  onChange={(e) => setEstimateQuantity(e.target.value)}
                  placeholder="e.g. 100"
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 flex text-sm font-medium text-muted-foreground">Cost per Unit (₹)</label>
                <input
                  type="number"
                  min="0"
                  value={costPerUnit}
                  onChange={(e) => setCostPerUnit(e.target.value)}
                  placeholder="e.g. 20"
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
              <div>
                <label className="mb-1 flex text-sm font-medium text-muted-foreground">Target Sell Price (₹)</label>
                <input
                  type="number"
                  min="0"
                  value={sellPrice}
                  onChange={(e) => setSellPrice(e.target.value)}
                  placeholder="e.g. 35"
                  className="w-full rounded-lg border border-border bg-background px-3 py-2 text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
                />
              </div>
            </div>
            {estimateQuantity && sellPrice && costPerUnit && (
              <div className="mt-4 flex flex-wrap gap-4 rounded-lg bg-accent p-3">
                <div className="flex-1 min-w-[150px]">
                  <p className="text-xs text-muted-foreground">Total Revenue</p>
                  <p className="font-bold text-foreground">₹{(Number(sellPrice) * Number(estimateQuantity)).toFixed(2)}</p>
                </div>
                <div className="flex-1 min-w-[150px]">
                  <p className="text-xs text-muted-foreground">Total Cost</p>
                  <p className="font-bold text-destructive">₹{(Number(costPerUnit) * Number(estimateQuantity)).toFixed(2)}</p>
                </div>
                <div className="flex-1 min-w-[150px]">
                  <p className="text-xs text-muted-foreground">Estimated Profit</p>
                  <p className="font-bold text-green-500">
                    ₹{((Number(sellPrice) - Number(costPerUnit)) * Number(estimateQuantity)).toFixed(2)}
                  </p>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((product) => {
            const latest = getLatestPrice(product.id, market.id);
            const isSelected = selected === product.id;
            return (
              <div
                key={product.id}
                className="cursor-pointer rounded-xl border border-border bg-card p-4 shadow-sm transition-all hover:shadow-md"
                onClick={() => setSelected(isSelected ? null : product.id)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-foreground">{product.name}</p>
                    <p className="text-xs text-muted-foreground">{product.category} • {product.unit}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <TrendIcon productId={product.id} />
                    <span className="text-lg font-bold text-primary">
                      ₹{latest?.price ?? "—"}
                    </span>
                  </div>
                </div>

                {isSelected && (
                  <div className="mt-4 border-t border-border pt-4">
                    <p className="mb-2 text-sm font-medium text-foreground">7-Day Price Trend</p>
                    <PriceChart productId={product.id} subMarketId={market.id} height={150} />
                    <div className="mt-3 flex items-start gap-2 rounded-lg bg-accent p-3">
                      <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-primary" />
                      <p className="text-xs text-foreground">
                        {getNegotiationInsight(product.id, market.id)}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
