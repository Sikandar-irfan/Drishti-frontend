
import { create } from 'zustand';
import { apiService, type BotTelemetry as ApiBotTelemetry, type BotLocation as ApiBotLocation } from '../services/apiService';

interface BotLocation {
  lat: number;
  lng: number;
}

interface BotTelemetry {
  battery: number;
  cpuUsage: number;
  temperature: number;
  fps: number;
  objectsDetected: number;
  status: 'idle' | 'patrolling' | 'alert' | 'offline';
}

interface BotState {
  isConnected: boolean;
  location: BotLocation;
  telemetry: BotTelemetry;
  streamUrl: string;
  pathHistory: BotLocation[];
  lastUpdate: number;
  initializeBot: () => void;
  updateTelemetry: (data: Partial<BotTelemetry>) => void;
  updateLocation: (location: BotLocation) => void;
  setStreamUrl: (url: string) => void;
  syncWithBackend: () => Promise<void>;
  checkConnection: () => Promise<boolean>;
}

export const useBotStore = create<BotState>((set, get) => ({
  isConnected: false,
  location: { lat: 12.9134, lng: 77.5204 }, // Rajarajeshwari Nagar, Bangalore coordinates
  telemetry: {
    battery: 85,
    cpuUsage: 45,
    temperature: 52,
    fps: 30,
    objectsDetected: 0,
    status: 'offline'
  },
  streamUrl: apiService.getStreamUrl(),
  pathHistory: [],
  lastUpdate: 0,

  initializeBot: async () => {
    const connected = await apiService.checkConnection();
    set({
      isConnected: connected,
      pathHistory: [{ lat: 12.9134, lng: 77.5204 }],
      streamUrl: apiService.getStreamUrl(),
      telemetry: connected ? get().telemetry : { ...get().telemetry, status: 'offline' }
    });
  },

  updateTelemetry: (data) => {
    set((state) => ({
      telemetry: { ...state.telemetry, ...data },
      lastUpdate: Date.now()
    }));
  },

  updateLocation: (location) => {
    set((state) => ({
      location,
      pathHistory: [...state.pathHistory.slice(-50), location],
      lastUpdate: Date.now()
    }));
  },

  setStreamUrl: (url) => {
    set({ streamUrl: url });
  },

  checkConnection: async () => {
    const connected = await apiService.checkConnection();
    set({ isConnected: connected });
    return connected;
  },

  syncWithBackend: async () => {
    try {
      // Check connection first
      const connected = await apiService.checkConnection();
      if (!connected) {
        set({ 
          isConnected: false,
          telemetry: { ...get().telemetry, status: 'offline' }
        });
        return;
      }

      // Fetch telemetry data
      const telemetryData = await apiService.getTelemetry();
      if (telemetryData) {
        set((state) => ({
          telemetry: {
            battery: telemetryData.battery,
            cpuUsage: telemetryData.cpuUsage,
            temperature: telemetryData.temperature,
            fps: telemetryData.fps,
            objectsDetected: telemetryData.objectsDetected,
            status: telemetryData.status
          },
          isConnected: true,
          lastUpdate: Date.now()
        }));
      }

      // Fetch location data
      const locationData = await apiService.getLocation();
      if (locationData) {
        const newLocation = { lat: locationData.lat, lng: locationData.lng };
        set((state) => ({
          location: newLocation,
          pathHistory: [...state.pathHistory.slice(-50), newLocation]
        }));
      }

    } catch (error) {
      console.error('Failed to sync with backend:', error);
      set({ 
        isConnected: false,
        telemetry: { ...get().telemetry, status: 'offline' }
      });
    }
  }
}));
