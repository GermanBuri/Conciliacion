import AccountBalanceWalletRoundedIcon from "@mui/icons-material/AccountBalanceWalletRounded";
import BalanceRoundedIcon from "@mui/icons-material/BalanceRounded";
import PendingActionsRoundedIcon from "@mui/icons-material/PendingActionsRounded";
import TaskAltRoundedIcon from "@mui/icons-material/TaskAltRounded";
import { Box, Grid, Paper, Typography } from "@mui/material";
import type { ElementType } from "react";

type KpiCard = {
  title: string;
  value: string;
  subtitle: string;
  icon: ElementType;
  accent: string;
  soft: string;
};

const cards: KpiCard[] = [
  {
    title: "Bancos",
    value: "0",
    subtitle: "Cuentas activas monitoreadas",
    icon: AccountBalanceWalletRoundedIcon,
    accent: "#2563eb",
    soft: "#dbeafe",
  },
  {
    title: "Contabilidad",
    value: "0",
    subtitle: "Registros contables cargados",
    icon: BalanceRoundedIcon,
    accent: "#0f766e",
    soft: "#ccfbf1",
  },
  {
    title: "Conciliadas",
    value: "0",
    subtitle: "Coincidencias resueltas",
    icon: TaskAltRoundedIcon,
    accent: "#7c3aed",
    soft: "#ede9fe",
  },
  {
    title: "Pendientes",
    value: "0",
    subtitle: "Movimientos por revisar",
    icon: PendingActionsRoundedIcon,
    accent: "#c2410c",
    soft: "#ffedd5",
  },
];

function StatsCards() {
  return (
    <Grid container spacing={3}>
      {cards.map(({ title, value, subtitle, icon: Icon, accent, soft }) => (
        <Grid key={title} size={{ xs: 12, sm: 6, xl: 3 }}>
          <Paper
            elevation={0}
            sx={{
              height: "100%",
              p: 3,
              borderRadius: 4,
              bgcolor: "#ffffff",
              boxShadow: "0 18px 40px rgba(15, 23, 42, 0.08)",
              border: "1px solid #dbe5f3",
            }}
          >
            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 2.5 }}>
              <Box>
                <Typography
                  variant="body2"
                  sx={{
                    color: "#64748b",
                    fontWeight: 700,
                    textTransform: "uppercase",
                    letterSpacing: "0.08em",
                  }}
                >
                  {title}
                </Typography>
                <Typography
                  variant="h3"
                  sx={{
                    mt: 1,
                    color: "#0f172a",
                    fontWeight: 800,
                    lineHeight: 1,
                  }}
                >
                  {value}
                </Typography>
              </Box>

              <Box
                sx={{
                  width: 56,
                  height: 56,
                  display: "grid",
                  placeItems: "center",
                  borderRadius: 3,
                  bgcolor: soft,
                  color: accent,
                }}
              >
                <Icon />
              </Box>
            </Box>

            <Typography variant="body2" sx={{ color: "#64748b" }}>
              {subtitle}
            </Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}

export default StatsCards;
