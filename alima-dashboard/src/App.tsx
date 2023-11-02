import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Home from "./pages/Home";
import PageNotFound from "./pages/PageNotFound";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/page-not-found" element={<PageNotFound />} />
      <Route
        path="*"
        element={<Navigate to="/page-not-found" replace={true} />}
      />
    </Routes>
  );
};

export default App;
