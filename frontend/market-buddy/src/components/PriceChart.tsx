import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getLast7DaysPrices } from "@/lib/data";

interface PriceChartProps {
  productId: string;
  subMarketId: string;
  height?: number;
}

export default function PriceChart({ productId, subMarketId, height = 180 }: PriceChartProps) {
  const data = getLast7DaysPrices(productId, subMarketId);

  const chartData = data.map((d) => ({
    date: new Date(d.date).toLocaleDateString("en-IN", { day: "numeric", month: "short" }),
    price: d.price,
  }));

  if (chartData.length === 0) {
    return <p className="py-8 text-center text-sm text-muted-foreground">No data available</p>;
  }

  const prices = chartData.map((d) => d.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const trend = prices[prices.length - 1] >= prices[0];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={chartData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id={`grad-${productId}-${subMarketId}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={trend ? "hsl(145, 63%, 32%)" : "hsl(0, 84%, 60%)"} stopOpacity={0.3} />
            <stop offset="95%" stopColor={trend ? "hsl(145, 63%, 32%)" : "hsl(0, 84%, 60%)"} stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis dataKey="date" tick={{ fontSize: 11, fill: "hsl(150, 10%, 45%)" }} axisLine={false} tickLine={false} />
        <YAxis domain={[min * 0.9, max * 1.1]} tick={{ fontSize: 11, fill: "hsl(150, 10%, 45%)" }} axisLine={false} tickLine={false} tickFormatter={(v) => `₹${v}`} />
        <Tooltip
          contentStyle={{ borderRadius: 12, border: "1px solid hsl(140, 15%, 88%)", fontSize: 13 }}
          formatter={(value: number) => [`₹${value}`, "Price"]}
        />
        <Area
          type="monotone"
          dataKey="price"
          stroke={trend ? "hsl(145, 63%, 32%)" : "hsl(0, 84%, 60%)"}
          strokeWidth={2}
          fill={`url(#grad-${productId}-${subMarketId})`}
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
