import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import CatalogoPage from "./pages/CatalogoPage";
import DetalheProdutoPage from "./pages/DetalheProdutoPage";
import NovoProdutoPage from "./pages/NovoProdutoPage";
import EditarProdutoPage from "./pages/EditarProdutoPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/produtos" replace />} />
        <Route path="/produtos" element={<CatalogoPage />} />
        <Route path="/produtos/novo" element={<NovoProdutoPage />} />
        <Route path="/produtos/:idProduto" element={<DetalheProdutoPage />} />
        <Route
          path="/produtos/:idProduto/editar"
          element={<EditarProdutoPage />}
        />
      </Routes>
    </BrowserRouter>
  );
}