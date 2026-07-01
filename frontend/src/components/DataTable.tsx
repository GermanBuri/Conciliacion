import MoreHorizRoundedIcon from "@mui/icons-material/MoreHorizRounded";
import VisibilityRoundedIcon from "@mui/icons-material/VisibilityRounded";
import { Box, Chip, IconButton, Paper, Typography } from "@mui/material";
import { DataGrid, type GridColDef } from "@mui/x-data-grid";

type Row = {
  id: number;
  fecha: string;
  banco: string;
  contabilidad: string;
  estado: "Conciliada" | "Pendiente" | "En revision";
  usuario: string;
};

const rows: Row[] = [
  { id: 1, fecha: "2026-07-01", banco: "Bancolombia", contabilidad: "Libro Mayor", estado: "Conciliada", usuario: "Administrador" },
  { id: 2, fecha: "2026-06-30", banco: "Davivienda", contabilidad: "Caja Principal", estado: "Pendiente", usuario: "Laura Ruiz" },
  { id: 3, fecha: "2026-06-29", banco: "BBVA", contabilidad: "Tesoreria", estado: "En revision", usuario: "Carlos Perez" },
  { id: 4, fecha: "2026-06-28", banco: "Banco de Bogota", contabilidad: "Cuentas por pagar", estado: "Conciliada", usuario: "Administrador" },
  { id: 5, fecha: "2026-06-27", banco: "Scotiabank", contabilidad: "Operaciones", estado: "Pendiente", usuario: "Martha Diaz" },
];

const statusStyles: Record<Row["estado"], { label: string; color: string; bg: string }> = {
  Conciliada: { label: "Conciliada", color: "#166534", bg: "#dcfce7" },
  Pendiente: { label: "Pendiente", color: "#9a3412", bg: "#ffedd5" },
  "En revision": { label: "En revision", color: "#1d4ed8", bg: "#dbeafe" },
};

const columns: GridColDef<Row>[] = [
  { field: "fecha", headerName: "Fecha", flex: 0.9, minWidth: 120 },
  { field: "banco", headerName: "Banco", flex: 1.2, minWidth: 150 },
  { field: "contabilidad", headerName: "Contabilidad", flex: 1.3, minWidth: 180 },
  {
    field: "estado",
    headerName: "Estado",
    flex: 1,
    minWidth: 150,
    sortable: false,
    renderCell: ({ value }) => {
      const status = statusStyles[value as Row["estado"]];

      return (
        <Chip
          label={status.label}
          size="small"
          sx={{
            bgcolor: status.bg,
            color: status.color,
            fontWeight: 700,
            borderRadius: 2,
          }}
        />
      );
    },
  },
  { field: "usuario", headerName: "Usuario", flex: 1.1, minWidth: 150 },
  {
    field: "acciones",
    headerName: "Acciones",
    flex: 0.8,
    minWidth: 130,
    sortable: false,
    filterable: false,
    renderCell: () => (
      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <IconButton size="small" sx={{ color: "#1d4ed8" }}>
          <VisibilityRoundedIcon fontSize="small" />
        </IconButton>
        <IconButton size="small" sx={{ color: "#64748b" }}>
          <MoreHorizRoundedIcon fontSize="small" />
        </IconButton>
      </Box>
    ),
  },
];

function DataTable() {
  return (
    <Paper
      elevation={0}
      sx={{
        p: 3,
        borderRadius: 4,
        bgcolor: "#ffffff",
        border: "1px solid #dbe5f3",
        boxShadow: "0 18px 40px rgba(15, 23, 42, 0.08)",
      }}
    >
      <Typography variant="h6" sx={{ mb: 2, color: "#0f172a", fontWeight: 700 }}>
        Conciliaciones recientes
      </Typography>

      <Box sx={{ height: 380 }}>
        <DataGrid
          rows={rows}
          columns={columns}
          disableRowSelectionOnClick
          hideFooterSelectedRowCount
          pageSizeOptions={[5]}
          initialState={{
            pagination: { paginationModel: { pageSize: 5, page: 0 } },
          }}
          sx={{
            border: "none",
            "& .MuiDataGrid-columnHeaders": {
              bgcolor: "#f8fbff",
              borderBottom: "1px solid #dbe5f3",
            },
            "& .MuiDataGrid-columnHeaderTitle": {
              color: "#334155",
              fontWeight: 700,
            },
            "& .MuiDataGrid-cell": {
              borderBottom: "1px solid #eef2f7",
              color: "#0f172a",
            },
            "& .MuiDataGrid-footerContainer": {
              borderTop: "1px solid #dbe5f3",
            },
          }}
        />
      </Box>
    </Paper>
  );
}

export default DataTable;
