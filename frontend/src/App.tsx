import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
} from "@mui/material";

function App() {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        background: "linear-gradient(135deg, #0f172a, #1e3a8a)",
      }}
    >
      <Container maxWidth="sm">
        <Card sx={{ borderRadius: 4, boxShadow: 8 }}>
          <CardContent sx={{ p: 5 }}>
            <Typography variant="h4" fontWeight="bold" align="center">
              ConciliarBT
            </Typography>

            <Typography align="center" color="text.secondary" sx={{ mt: 1, mb: 4 }}>
              Plataforma empresarial de conciliación bancaria
            </Typography>

            <TextField label="Correo electrónico" fullWidth margin="normal" />

            <TextField
              label="Contraseña"
              type="password"
              fullWidth
              margin="normal"
            />

            <Button
              variant="contained"
              fullWidth
              size="large"
              sx={{ mt: 3, py: 1.3, borderRadius: 2 }}
            >
              Iniciar sesión
            </Button>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

export default App;