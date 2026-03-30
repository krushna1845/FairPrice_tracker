import { MapPin, Clock, ArrowLeft, Search, Plus } from "lucide-react";
import { getSubMarkets, addSubMarket, type SubMarket, type Role } from "@/lib/data";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";

interface MarketSelectionProps {
  onSelect: (market: SubMarket) => void;
  onBack: () => void;
  title: string;
  role?: Role;
}

export default function MarketSelection({ onSelect, onBack, title, role }: MarketSelectionProps) {
  const [search, setSearch] = useState("");
  const [markets, setMarkets] = useState<SubMarket[]>([]);
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [newMarketName, setNewMarketName] = useState("");
  const [newMarketArea, setNewMarketArea] = useState("");

  useEffect(() => {
    setMarkets(getSubMarkets());
  }, []);

  const filtered = markets.filter(
    (m) =>
      m.name.toLowerCase().includes(search.toLowerCase()) ||
      m.area.toLowerCase().includes(search.toLowerCase())
  );

  const handleAddMarket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMarketName || !newMarketArea) return;
    const added = addSubMarket(newMarketName, newMarketArea);
    setMarkets((prev) => [...prev, added]);
    setNewMarketName("");
    setNewMarketArea("");
    setIsAddOpen(false);
  };

  return (
    <div className="min-h-screen px-4 py-6">
      <div className="mx-auto max-w-3xl">
        <button onClick={onBack} className="mb-4 flex items-center gap-2 text-muted-foreground hover:text-foreground">
          <ArrowLeft className="h-5 w-5" />
        </button>
        <div className="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-foreground">{title}</h2>
            <p className="text-sm text-muted-foreground">Mumbai Market — Select a sub-market</p>
          </div>
          {role === "vendor" && (
            <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
              <DialogTrigger asChild>
                <Button className="bg-vendor hover:bg-vendor/90 text-vendor-foreground gap-2">
                  <Plus className="h-4 w-4" /> Add Market
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle>Add New Mumbai Market</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleAddMarket} className="space-y-4 pt-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Market Name</Label>
                    <Input
                      id="name"
                      placeholder="e.g. Borivali Market"
                      value={newMarketName}
                      onChange={(e) => setNewMarketName(e.target.value)}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="area">Area in Mumbai</Label>
                    <Input
                      id="area"
                      placeholder="e.g. Borivali West"
                      value={newMarketArea}
                      onChange={(e) => setNewMarketArea(e.target.value)}
                      required
                    />
                  </div>
                  <Button type="submit" className="w-full bg-vendor hover:bg-vendor/90 text-vendor-foreground">
                    Add Market
                  </Button>
                </form>
              </DialogContent>
            </Dialog>
          )}
        </div>

        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search by market name or area..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full rounded-xl border border-border bg-card py-3 pl-10 pr-4 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          {filtered.map((market) => (
            <button
              key={market.id}
              onClick={() => onSelect(market)}
              className="flex items-start gap-4 rounded-xl border border-border bg-card p-5 text-left shadow-sm transition-all hover:border-primary/30 hover:shadow-md"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-accent">
                <MapPin className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="font-semibold text-foreground">{market.name}</p>
                <p className="text-sm text-muted-foreground">{market.area}, Mumbai</p>
                <p className="mt-1 flex items-center gap-1 text-xs text-muted-foreground">
                  <Clock className="h-3 w-3" /> Updated today
                </p>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
