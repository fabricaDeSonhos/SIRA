"use client";
import { createContext, useContext, useState } from "react";

const LoginContext = createContext();

export function LoginProvider({ children }) {
  const [logado, setLogado] = useState(false);
  const [usuario, setUsuario] = useState("");

  const login = (nome, senha) => {
    if (nome === "admin" && senha === "123") {
      setLogado(true);
      setUsuario(nome);
      return true;
    }
    return false;
  };

  const logout = () => {
    setLogado(false);
    setUsuario("");
  };

  return (
    <LoginContext.Provider value={{ logado, login, logout, usuario }}>
      {children}
    </LoginContext.Provider>
  );
}

export function useLogin() {
  return useContext(LoginContext);
}