import SearchBar from "@/components/search/SearchBar";
import WelcomeText from "../WelcomeText";

export default function SearchSection() {
  return (
    <div className="relative flex min-h-screen flex-col justify-center p-4">
      <div className="relative z-10 mx-auto w-full max-w-2xl">
        <WelcomeText />
        <SearchBar />
      </div>
    </div>
  );
}
