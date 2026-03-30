import { Sprout, Store, ShoppingCart } from "lucide-react";
import type { Role } from "@/lib/data";

interface RoleSelectionProps {
  onSelect: (role: Role) => void;
}

const roles = [
  {
    id: "farmer" as Role,
    label: "Farmer",
    description: "View prices & get negotiation tips",
    icon: Sprout,
  },
  {
    id: "vendor" as Role,
    label: "Vendor",
    description: "Update & manage market prices",
    icon: Store,
  },
  {
    id: "consumer" as Role,
    label: "Consumer",
    description: "Compare prices across markets",
    icon: ShoppingCart,
  },
];

export default function RoleSelection({ onSelect }: RoleSelectionProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4">
      <h1 className="mb-2 text-4xl font-bold text-primary md:text-5xl">FairPrice Tracker</h1>
      <p className="mb-10 text-muted-foreground">Real market prices for everyone</p>
      <div className="grid w-full max-w-3xl grid-cols-1 gap-5 sm:grid-cols-3">
        {roles.map((role) => (
          <button
            key={role.id}
            onClick={() => onSelect(role.id)}
            className="group flex flex-col items-center gap-3 rounded-xl border border-border bg-card p-8 shadow-sm transition-all hover:border-primary/30 hover:shadow-md"
          >
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-accent">
              <role.icon className="h-8 w-8 text-primary" />
            </div>
            <span className="text-lg font-semibold text-foreground">{role.label}</span>
            <span className="text-sm text-muted-foreground">{role.description}</span>
          </button>
        ))}
      </div>
      <p className="mt-10 text-sm text-muted-foreground">
        Community-driven • Real prices • Fair trade
      </p>
    </div>
  );
}
