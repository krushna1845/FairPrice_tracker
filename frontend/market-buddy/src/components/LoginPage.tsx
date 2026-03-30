import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Lock, User, Mail } from "lucide-react";
import { authAPI } from "@/services/api";

interface LoginPageProps {
  onLogin: () => void;
}

const LoginPage = ({ onLogin }: LoginPageProps) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      let response;
      if (isRegistering) {
        response = await authAPI.register(name, email, password);
      } else {
        response = await authAPI.login(email, password);
      }
      
      // Store JWT token
      localStorage.setItem("access_token", response.data.access_token);
      
      // Store user info
      localStorage.setItem(
        "user",
        JSON.stringify({
          id: response.data.user_id,
          name: response.data.name,
          email: response.data.email,
        })
      );

      // Call parent callback
      sessionStorage.setItem("authenticated", "true");
      onLogin();
    } catch (err: any) {
      if (err.response?.status === 422) {
         // Pydantic validation error mapping
         const details = err.response.data.detail;
         if (Array.isArray(details) && details.length > 0) {
            setError(`Validation error: ${details[0].msg}`);
         } else {
            setError("Invalid input data format.");
         }
      } else {
         const errorMessage = err.response?.data?.detail || "Authentication failed. Please try again.";
         setError(typeof errorMessage === 'string' ? errorMessage : "An error occurred.");
      }
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/10 via-background to-accent/10 flex items-center justify-center p-4">
      <Card className="w-full max-w-sm shadow-xl border-primary/20">
        <CardHeader className="text-center space-y-1">
          <div className="mx-auto w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center mb-2">
            {isRegistering ? <User className="w-7 h-7 text-primary" /> : <Lock className="w-7 h-7 text-primary" />}
          </div>
          <CardTitle className="font-heading text-2xl">FairPrice Tracker</CardTitle>
          <CardDescription>{isRegistering ? "Create a new account" : "Sign in to continue"}</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {isRegistering && (
                <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    id="name"
                    placeholder="Enter full name"
                    value={name}
                    onChange={(e) => { setName(e.target.value); setError(""); }}
                    className="pl-9"
                    required
                  />
                </div>
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email Address / Username</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="text"
                  placeholder="Enter email or username"
                  value={email}
                  onChange={(e) => { setEmail(e.target.value); setError(""); }}
                  className="pl-9"
                  required
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  placeholder={isRegistering ? "Choose a password" : "Enter password"}
                  value={password}
                  onChange={(e) => { setPassword(e.target.value); setError(""); }}
                  className="pl-9"
                  required
                />
              </div>
            </div>
            {error && <p className="text-sm text-destructive text-center">{error}</p>}
            <div className="flex flex-col gap-2 pt-2">
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? (isRegistering ? "Registering..." : "Signing in...") : (isRegistering ? "Sign Up" : "Sign In")}
              </Button>
              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={() => {
                  sessionStorage.setItem("authenticated", "guest");
                  onLogin();
                }}
              >
                Continue as Guest
              </Button>
            </div>
          </form>
        </CardContent>
        <CardFooter className="justify-center border-t pt-4">
             <Button variant="link" onClick={() => { setIsRegistering(!isRegistering); setError(""); }} className="text-sm text-muted-foreground">
                 {isRegistering ? "Already have an account? Sign In" : "Don't have an account? Sign Up"}
             </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default LoginPage;
