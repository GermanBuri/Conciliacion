import NotificationsNoneRoundedIcon from "@mui/icons-material/NotificationsNoneRounded";
import { Avatar, Badge, Box, IconButton, Paper, Typography } from "@mui/material";

type TopbarProps = {
  height: number;
};

function Topbar({ height }: TopbarProps) {
  return (
    <Paper
      elevation={0}
      square
      sx={{
        position: "sticky",
        top: 0,
        zIndex: 10,
        height,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        px: { xs: 2, md: 4 },
        borderBottom: "1px solid #d8e2f0",
        bgcolor: "rgba(248, 251, 255, 0.96)",
        backdropFilter: "blur(10px)",
      }}
    >
      <Box>
        <Typography variant="h6" sx={{ color: "#0f172a", fontWeight: 700 }}>
          Bienvenido
        </Typography>
        <Typography variant="body2" sx={{ color: "#64748b" }}>
          Usuario Administrador
        </Typography>
      </Box>

      <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
        <IconButton
          sx={{
            width: 44,
            height: 44,
            bgcolor: "#e8f0fe",
            color: "#1d4ed8",
            "&:hover": { bgcolor: "#dbeafe" },
          }}
        >
          <Badge color="error" variant="dot">
            <NotificationsNoneRoundedIcon />
          </Badge>
        </IconButton>

        <Avatar
          sx={{
            width: 44,
            height: 44,
            bgcolor: "#1d4ed8",
            fontWeight: 700,
          }}
        >
          UA
        </Avatar>
      </Box>
    </Paper>
  );
}

export default Topbar;
