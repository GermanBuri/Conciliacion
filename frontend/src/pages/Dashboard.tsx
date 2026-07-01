import AccessTimeRoundedIcon from "@mui/icons-material/AccessTimeRounded";
import DownloadRoundedIcon from "@mui/icons-material/DownloadRounded";
import SyncAltRoundedIcon from "@mui/icons-material/SyncAltRounded";
import UploadFileRoundedIcon from "@mui/icons-material/UploadFileRounded";
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from "chart.js";
import { Doughnut } from "react-chartjs-2";
import { Box, Grid, List, ListItem, ListItemIcon, ListItemText, Paper, Typography } from "@mui/material";

import DataTable from "../components/DataTable";
import StatsCards from "../components/StatsCards";
import DashboardLayout from "../layouts/DashboardLayout";

ChartJS.register(ArcElement, Tooltip, Legend);

const doughnutData = {
  labels: ["Conciliadas", "Pendientes"],
  datasets: [
    {
      data: [72, 28],
      backgroundColor: ["#2563eb", "#93c5fd"],
      borderColor: ["#2563eb", "#93c5fd"],
      borderWidth: 0,
      hoverOffset: 8,
    },
  ],
};

const doughnutOptions = {
  cutout: "72%",
  plugins: {
    legend: {
      position: "bottom" as const,
      labels: {
        color: "#475569",
        boxWidth: 12,
        usePointStyle: true,
        pointStyle: "circle" as const,
        padding: 18,
      },
    },
  },
};

const recentActivity = [
  { label: "Carga banco", detail: "Extracto de Bancolombia cargado", icon: UploadFileRoundedIcon, color: "#2563eb", bg: "#dbeafe" },
  { label: "Carga contable", detail: "Archivo de libro mayor actualizado", icon: UploadFileRoundedIcon, color: "#0f766e", bg: "#ccfbf1" },
  { label: "Conciliacion", detail: "Proceso automatico ejecutado", icon: SyncAltRoundedIcon, color: "#7c3aed", bg: "#ede9fe" },
  { label: "Exportacion", detail: "Reporte Excel generado", icon: DownloadRoundedIcon, color: "#c2410c", bg: "#ffedd5" },
];

const panelSx = {
  p: 3,
  borderRadius: 4,
  bgcolor: "#ffffff",
  border: "1px solid #dbe5f3",
  boxShadow: "0 18px 40px rgba(15, 23, 42, 0.08)",
};

function Dashboard() {
  return (
    <DashboardLayout>
      <Box sx={{ maxWidth: 1440, mx: "auto" }}>
        <Typography variant="h4" sx={{ mb: 3, color: "#0f172a", fontWeight: 800 }}>
          Dashboard
        </Typography>

        <StatsCards />

        <Grid container spacing={3} sx={{ mt: 0.5 }}>
          <Grid size={{ xs: 12, xl: 7 }}>
            <Paper elevation={0} sx={{ ...panelSx, minHeight: 360 }}>
              <Typography variant="h6" sx={{ color: "#0f172a", fontWeight: 700 }}>
                Estado de conciliaciones
              </Typography>
              <Typography variant="body2" sx={{ mt: 0.5, color: "#64748b" }}>
                Balance consolidado entre movimientos conciliados y pendientes.
              </Typography>

              <Box
                sx={{
                  mt: 3,
                  maxWidth: 360,
                  mx: "auto",
                }}
              >
                <Doughnut data={doughnutData} options={doughnutOptions} />
              </Box>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, xl: 5 }}>
            <Paper elevation={0} sx={{ ...panelSx, minHeight: 360 }}>
              <Typography variant="h6" sx={{ color: "#0f172a", fontWeight: 700 }}>
                Actividad reciente
              </Typography>
              <Typography variant="body2" sx={{ mt: 0.5, color: "#64748b" }}>
                Eventos recientes del flujo operativo de conciliacion.
              </Typography>

              <List sx={{ mt: 2, display: "grid", gap: 1.5 }}>
                {recentActivity.map(({ label, detail, icon: Icon, color, bg }) => (
                  <ListItem
                    key={label}
                    disableGutters
                    sx={{
                      px: 1.5,
                      py: 1.25,
                      borderRadius: 3,
                      border: "1px solid #e2e8f0",
                      bgcolor: "#fbfdff",
                    }}
                  >
                    <ListItemIcon sx={{ minWidth: 48 }}>
                      <Box
                        sx={{
                          width: 38,
                          height: 38,
                          display: "grid",
                          placeItems: "center",
                          borderRadius: 2.5,
                          bgcolor: bg,
                          color,
                        }}
                      >
                        <Icon fontSize="small" />
                      </Box>
                    </ListItemIcon>
                    <ListItemText
                      primary={label}
                      secondary={detail}
                      primaryTypographyProps={{
                        color: "#0f172a",
                        fontWeight: 700,
                        fontSize: 15,
                      }}
                      secondaryTypographyProps={{
                        color: "#64748b",
                        fontSize: 13,
                      }}
                    />
                    <AccessTimeRoundedIcon sx={{ color: "#94a3b8", fontSize: 18 }} />
                  </ListItem>
                ))}
              </List>
            </Paper>
          </Grid>
        </Grid>

        <Box sx={{ mt: 3 }}>
          <DataTable />
        </Box>
      </Box>
    </DashboardLayout>
  );
}

export default Dashboard;
