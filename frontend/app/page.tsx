"use client";

import { useState, useEffect, useCallback } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Usuario {
  id: number;
  name: string;
  lastname: string;
  email: string;
}

interface FormData {
  name: string;
  lastname: string;
  email: string;
}

const emptyForm: FormData = { name: "", lastname: "", email: "" };

export default function Home() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<Usuario | null>(null);
  const [formData, setFormData] = useState<FormData>(emptyForm);
  const [submitting, setSubmitting] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const fetchUsuarios = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_URL}/usuarios`);
      if (!res.ok) throw new Error(`Error ${res.status}`);
      const data: Usuario[] = await res.json();
      setUsuarios(data);
    } catch {
      setError("No se pudo conectar con la API. ¿Está corriendo el backend?");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsuarios();
  }, [fetchUsuarios]);

  const openCreate = () => {
    setEditingUser(null);
    setFormData(emptyForm);
    setFormError(null);
    setModalOpen(true);
  };

  const openEdit = (user: Usuario) => {
    setEditingUser(user);
    setFormData({
      name: user.name,
      lastname: user.lastname,
      email: user.email,
    });
    setFormError(null);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setEditingUser(null);
    setFormData(emptyForm);
    setFormError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setFormError(null);
    try {
      const url = editingUser
        ? `${API_URL}/usuarios/${editingUser.id}`
        : `${API_URL}/usuarios`;
      const method = editingUser ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.detail || `Error ${res.status}`);
      }

      closeModal();
      await fetchUsuarios();
    } catch (err: unknown) {
      setFormError(
        err instanceof Error ? err.message : "Error al guardar el usuario",
      );
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      const res = await fetch(`${API_URL}/usuarios/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error(`Error ${res.status}`);
      setDeleteConfirm(null);
      await fetchUsuarios();
    } catch {
      setError("No se pudo eliminar el usuario.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-5xl mx-auto px-4 py-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Administrador de Usuarios
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              {loading
                ? "Cargando..."
                : `${usuarios.length} usuario(s) registrado(s)`}
            </p>
          </div>
          <button
            onClick={openCreate}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium text-sm transition-colors cursor-pointer"
          >
            + Nuevo Usuario
          </button>
        </div>

        {/* Error banner */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6 flex items-center justify-between">
            <span className="text-sm">{error}</span>
            <button
              onClick={() => setError(null)}
              className="text-red-400 hover:text-red-600 ml-4 text-lg leading-none cursor-pointer"
            >
              ×
            </button>
          </div>
        )}

        {/* Table card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {loading ? (
            <div className="p-16 text-center">
              <div className="inline-block w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mb-3" />
              <p className="text-sm text-gray-400">Cargando usuarios...</p>
            </div>
          ) : usuarios.length === 0 ? (
            <div className="p-16 text-center text-gray-400">
              <p className="text-sm">No hay usuarios registrados.</p>
              <button
                onClick={openCreate}
                className="mt-3 text-sm text-blue-600 hover:underline cursor-pointer"
              >
                Crear el primero
              </button>
            </div>
          ) : (
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  {["ID", "Nombre", "Apellido", "Email", "Acciones"].map(
                    (h) => (
                      <th
                        key={h}
                        className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wider px-6 py-3"
                      >
                        {h}
                      </th>
                    ),
                  )}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {usuarios.map((u) => (
                  <tr key={u.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm text-gray-400">#{u.id}</td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      {u.name}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {u.lastname}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {u.email}
                    </td>
                    <td className="px-6 py-4">
                      {deleteConfirm === u.id ? (
                        <div className="flex items-center gap-3">
                          <span className="text-xs text-gray-600">
                            ¿Confirmar?
                          </span>
                          <button
                            onClick={() => handleDelete(u.id)}
                            className="text-xs text-red-600 font-semibold hover:underline cursor-pointer"
                          >
                            Sí, eliminar
                          </button>
                          <button
                            onClick={() => setDeleteConfirm(null)}
                            className="text-xs text-gray-500 hover:underline cursor-pointer"
                          >
                            Cancelar
                          </button>
                        </div>
                      ) : (
                        <div className="flex items-center gap-4">
                          <button
                            onClick={() => openEdit(u)}
                            className="text-sm text-blue-600 hover:text-blue-800 font-medium cursor-pointer"
                          >
                            Editar
                          </button>
                          <button
                            onClick={() => setDeleteConfirm(u.id)}
                            className="text-sm text-red-500 hover:text-red-700 font-medium cursor-pointer"
                          >
                            Eliminar
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Modal */}
      {modalOpen && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={(e) => e.target === e.currentTarget && closeModal()}
        >
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md">
            {/* Modal header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h2 className="text-base font-semibold text-gray-900">
                {editingUser ? "Editar Usuario" : "Nuevo Usuario"}
              </h2>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-gray-600 text-xl leading-none cursor-pointer"
              >
                ×
              </button>
            </div>

            {/* Modal form */}
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              {formError && (
                <div className="bg-red-50 border border-red-200 text-red-600 text-sm px-3 py-2 rounded-lg">
                  {formError}
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Nombre
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Nombre"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Apellido
                </label>
                <input
                  type="text"
                  required
                  value={formData.lastname}
                  onChange={(e) =>
                    setFormData({ ...formData, lastname: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Apellido"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="w-full border border-gray-300 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="correo@ejemplo.com"
                />
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white py-2.5 rounded-lg font-medium text-sm transition-colors cursor-pointer"
                >
                  {submitting
                    ? "Guardando..."
                    : editingUser
                      ? "Actualizar"
                      : "Crear Usuario"}
                </button>
                <button
                  type="button"
                  onClick={closeModal}
                  className="flex-1 border border-gray-300 text-gray-700 py-2.5 rounded-lg font-medium text-sm hover:bg-gray-50 transition-colors cursor-pointer"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
