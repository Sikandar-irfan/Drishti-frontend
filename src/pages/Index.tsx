
import { useEffect, useRef } from 'react';
import { VideoStreamPanel } from '@/components/VideoStreamPanel';
import { MapPanel } from '@/components/MapPanel';
import { TelemetryPanel } from '@/components/TelemetryPanel';
import { Header } from '@/components/Header';
import { useBotStore } from '@/store/botStore';

const Index = () => {
  const { initializeBot, syncWithBackend, checkConnection, isConnected } = useBotStore();
  const syncIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    // Initialize bot data
    const initialize = async () => {
      await initializeBot();
      
      // Start real-time sync with backend
      syncIntervalRef.current = setInterval(async () => {
        await syncWithBackend();
      }, 2000); // Sync every 2 seconds
    };

    initialize();

    // Cleanup interval on unmount
    return () => {
      if (syncIntervalRef.current) {
        clearInterval(syncIntervalRef.current);
      }
    };
  }, [initializeBot, syncWithBackend]);

  // Connection monitoring
  useEffect(() => {
    const connectionCheck = setInterval(async () => {
      await checkConnection();
    }, 10000); // Check connection every 10 seconds

    return () => clearInterval(connectionCheck);
  }, [checkConnection]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <Header />
      
      {/* Connection Status Banner */}
      {!isConnected && (
        <div className="bg-red-600/90 text-white text-center py-2 px-4">
          <span className="text-sm font-medium">
            ⚠️ Backend Offline - Attempting to reconnect to Raspberry Pi (192.168.0.101)...
          </span>
        </div>
      )}
      
      <main className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-8rem)]">
          {/* Video Stream Panel */}
          <div className="lg:col-span-1">
            <VideoStreamPanel />
          </div>
          
          {/* Map Panel */}
          <div className="lg:col-span-1">
            <MapPanel />
          </div>
          
          {/* Telemetry Panel */}
          <div className="lg:col-span-1">
            <TelemetryPanel />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
