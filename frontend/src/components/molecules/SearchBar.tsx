import { useState } from "react";

import Button from "../atoms/Button";
import Input from "../atoms/Input";

type SearchBarProps = {
  defaultValue?: string;
  loading?: boolean;
  placeholder?: string;
  onSearch: (term: string) => void;
};

export default function SearchBar({
  defaultValue = "",
  loading = false,
  placeholder = "Buscar por nome ou categoria",
  onSearch,
}: SearchBarProps) {
  const [value, setValue] = useState(defaultValue);

  function handleSearch() {
    onSearch(value);
  }

  return (
    <div className="flex w-full flex-col gap-3 sm:flex-row">
      <Input
        value={value}
        placeholder={placeholder}
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            handleSearch();
          }
        }}
        className="sm:min-w-[340px]"
      />

      <Button
        type="button"
        variant="dark"
        onClick={handleSearch}
        disabled={loading}
      >
        {loading ? "Buscando..." : "Buscar"}
      </Button>
    </div>
  );
}