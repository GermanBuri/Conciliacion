import type { ReactNode } from "react";
import { Box } from "@mui/material";

import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

const SIDEBAR_WIDTH = 260;
const TOPBAR_HEIGHT = 70;
const pageBackground = "#eef3fb";

type DashboardLayoutProps = {
  children: ReactNode;
};

function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: pageBackground }}>
      <Sidebar width={SIDEBAR_WIDTH} />

      <Box
        sx={{
          minHeight: "100vh",
          ml: { md: `${SIDEBAR_WIDTH}px` },
        }}
      >
        <Topbar height={TOPBAR_HEIGHT} />

        <Box
          component="main"
          sx={{
            minHeight: `calc(100vh - ${TOPBAR_HEIGHT}px)`,
            px: { xs: 2, md: 4 },
            py: { xs: 3, md: 4 },
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
}

export default DashboardLayout;
