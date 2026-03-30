import { ArrowLeft } from "lucide-react";
import { PRODUCTS, getSubMarkets, getLatestPrice, type SubMarket } from "@/lib/data";
import PriceChart from "./PriceChart";
import { useState } from "react";

interface ConsumerViewProps {
  market: SubMarket;
  onBack: () => void;
}

const CATEGORIES = ["All", "Fruit", "Vegetable", "Grain", "Spice"] as const;

export default function ConsumerView({ market, onBack }: ConsumerViewProps) {
  const [category, setCategory] = useState<string>("All");
  const [selected, setSelected] = useState<string | null>(null);

  const filtered = PRODUCTS.filter((p) => category === "All" || p.category === category);

  return (
    <div className="min-h-screen px-4 py-6">
      <div className="mx-auto max-w-4xl">
        <button onClick={onBack} className="mb-4 flex items-center gap-2 text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h2 className="text-2xl font-bold text-foreground">{market.name}</h2>
        <p className="mb-6 text-sm text-muted-foreground">{market.area}, Mumbai — Compare Prices</p>

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

        <div className="space-y-4">
          {filtered.map((product) => {
            const isOpen = selected === product.id;
            // Compare across all sub-markets
            const comparisons = getSubMarkets().map((m) => ({
              market: m,
              price: getLatestPrice(product.id, m.id),
            })).filter((c) => c.price);

            const prices = comparisons.map((c) => c.price!.price);
            const cheapest = prices.length ? Math.min(...prices) : 0;

            return (
              <div
                key={product.id}
                className="rounded-xl border border-border bg-card shadow-sm"
              >
                <button
                  onClick={() => setSelected(isOpen ? null : product.id)}
                  className="flex w-full items-center justify-between p-4 text-left"
                >
                  <div>
                    <p className="font-semibold text-foreground">{product.name}</p>
                    <p className="text-xs text-muted-foreground">{product.category} • {product.unit}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-muted-foreground">Best price</p>
                    <p className="text-lg font-bold text-primary">₹{cheapest || "—"}</p>
                    {cheapest > 0 && (
                      <p className="text-[10px] text-muted-foreground">
                        {(() => {
                          const bestPriceObj = comparisons.find(c => c.price?.price === cheapest)?.price;
                          if (!bestPriceObj?.updatedAt) return "";
                          const diffHours = Math.floor((Date.now() - new Date(bestPriceObj.updatedAt).getTime()) / (1000 * 60 * 60));
                          if (diffHours < 1) return "Updated just now";
                          return `Last updated: ${diffHours} hr${diffHours > 1 ? 's' : ''} ago`;
                        })()}
                      </p>
                    )}
                  </div>
                </button>

                {isOpen && (
                  <div className="border-t border-border p-4">
                    <p className="mb-3 text-sm font-medium text-foreground">Price across markets</p>
                    <div className="mb-4 space-y-2">
                      {comparisons
                        .sort((a, b) => (a.price?.price ?? 0) - (b.price?.price ?? 0))
                        .map((c) => (
                          <div
                            key={c.market.id}
                            className={`flex items-center justify-between rounded-lg p-3 ${
                              c.price?.price === cheapest
                                ? "bg-accent border border-primary/20"
                                : "bg-muted"
                            }`}
                          >
                            <span className="text-sm text-foreground">{c.market.name}</span>
                            <span
                              className={`font-semibold ${
                                c.price?.price === cheapest ? "text-primary" : "text-foreground"
                              }`}
                            >
                              ₹{c.price?.price}
                              {c.price?.price === cheapest && (
                                <span className="ml-1 text-xs font-normal text-primary">Best</span>
                              )}
                            </span>
                          </div>
                        ))}
                    </div>
                    <p className="mb-2 text-sm font-medium text-foreground">
                      7-Day Trend at {market.name}
                    </p>
                    <PriceChart productId={product.id} subMarketId={market.id} height={150} />
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
