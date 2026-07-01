import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import DashboardIcon from "@mui/icons-material/Dashboard";
import HistoryIcon from "@mui/icons-material/History";
import PeopleIcon from "@mui/icons-material/People";
import SettingsIcon from "@mui/icons-material/Settings";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { Box, List, ListItemButton, ListItemIcon, ListItemText, Typography } from "@mui/material";

const menuItems = [
  { label: "Dashboard", icon: DashboardIcon, active: true },
  { label: "Subidas", icon: UploadFileIcon },
  { label: "Conciliaciones", icon: AccountBalanceIcon },
  { label: "Auditoria", icon: HistoryIcon },
  { label: "Usuarios", icon: PeopleIcon },
  { label: "Configuracion", icon: SettingsIcon },
];

type SidebarProps = {
  width: number;
};

function Sidebar({ width }: SidebarProps) {
  return (
    <Box
      component="aside"
      sx={{
        position: { md: "fixed" },
        top: 0,
        left: 0,
        width: { xs: "100%", md: width },
        height: { md: "100vh" },
        px: 2,
        py: 3,
        bgcolor: "#0f274d",
        color: "#f8fbff",
        borderRight: "1px solid rgba(148, 163, 184, 0.14)",
      }}
    >
      <Box
        sx={{
          px: 1.5,
          pb: 3,
          borderBottom: "1px solid rgba(226, 232, 240, 0.12)",
        }}
      >
        <Typography variant="h5" sx={{ fontWeight: 800, letterSpacing: "0.03em" }}>
          ConciliarBT
        </Typography>
        <Typography variant="body2" sx={{ mt: 1, color: "rgba(226, 232, 240, 0.72)" }}>
          Plataforma empresarial
        </Typography>
      </Box>

      <List sx={{ mt: 2, display: "grid", gap: 1 }}>
        {menuItems.map(({ label, icon: Icon, active }) => (
          <ListItemButton
            key={label}
            sx={{
              minHeight: 52,
              borderRadius: 3,
              px: 1.5,
              color: active ? "#ffffff" : "rgba(226, 232, 240, 0.84)",
              bgcolor: active ? "rgba(59, 130, 246, 0.28)" : "transparent",
              border: active ? "1px solid rgba(96, 165, 250, 0.42)" : "1px solid transparent",
              "&:hover": {
                bgcolor: "rgba(59, 130, 246, 0.18)",
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: "inherit" }}>
              <Icon fontSize="small" />
            </ListItemIcon>
            <ListItemText
              primary={label}
              primaryTypographyProps={{
                fontSize: 15,
                fontWeight: active ? 700 : 500,
              }}
            />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );
}

export default Sidebar;
