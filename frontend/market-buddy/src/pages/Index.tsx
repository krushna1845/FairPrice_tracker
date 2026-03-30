import { useState } from "react";
import LoginPage from "@/components/LoginPage";
import RoleSelection from "@/components/RoleSelection";
import MarketSelection from "@/components/MarketSelection";
import FarmerView from "@/components/FarmerView";
import VendorView from "@/components/VendorView";
import ConsumerView from "@/components/ConsumerView";
import type { Role, SubMarket } from "@/lib/data";

type Screen = "login" | "role" | "market" | "dashboard";

const Index = () => {
  const [screen, setScreen] = useState<Screen>("role");
  const [role, setRole] = useState<Role | null>(null);
  const [market, setMarket] = useState<SubMarket | null>(null);

  const handleRoleSelect = (r: Role) => {
    setRole(r);
    if (r === "vendor" && !sessionStorage.getItem("authenticated")) {
      setScreen("login");
    } else {
      setScreen("market");
    }
  };

  const handleMarketSelect = (m: SubMarket) => {
    setMarket(m);
    setScreen("dashboard");
  };

  const handleLogin = () => {
    setScreen("market");
  };

  const titles: Record<Role, string> = {
    farmer: "View Market Prices",
    vendor: "Update Market Prices",
    consumer: "Compare Prices",
  };

  if (screen === "login") return <LoginPage onLogin={handleLogin} />;

  if (screen === "role") return <RoleSelection onSelect={handleRoleSelect} />;

  if (screen === "market" && role)
    return (
      <MarketSelection
        title={titles[role]}
        onSelect={handleMarketSelect}
        onBack={() => setScreen("role")}
        role={role}
      />
    );

  if (screen === "dashboard" && role && market) {
    const backToMarket = () => setScreen("market");
    if (role === "farmer") return <FarmerView market={market} onBack={backToMarket} />;
    if (role === "vendor") return <VendorView market={market} onBack={backToMarket} />;
    if (role === "consumer") return <ConsumerView market={market} onBack={backToMarket} />;
  }

  return null;
};

export default Index;
