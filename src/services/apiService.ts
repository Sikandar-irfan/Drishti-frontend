/**
 * API Service for Raspberry Pi Backend Communication
 * Handles all communication between React frontend and autonomous navigation system
 */

export interface ApiConfig {
  baseUrl: string;
  streamUrl: string;
  updateInterval: number;
}

export interface BotTelemetry {
  battery: number;
  cpuUsage: number;
  temperature: number;
  fps: number;
  objectsDetected: number;
  status: 'idle' | 'patrolling' | 'alert' | 'offline';
  timestamp: string;
}

export interface BotLocation {
  lat: number;
  lng: number;
  heading?: number;
  speed?: number;
  timestamp: string;
}

export interface SystemStatus {
  connected: boolean;
  systemHealth: 'good' | 'warning' | 'critical';
  uptime: number;
  version: string;
}

export interface SlamData {
  map: Array<{x: number, y: number, z: number}>;
  pose: {x: number, y: number, z: number, roll: number, pitch: number, yaw: number};
  landmarks: Array<{id: string, x: number, y: number, confidence: number}>;
}

export interface VoiceStatus {
  isListening: boolean;
  lastCommand: string;
  language: string;
  confidence: number;
}

class ApiService {
  private config: ApiConfig;
  private isConnected: boolean = false;

  constructor() {
    this.config = {
      baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://192.168.0.101:5000',
      streamUrl: import.meta.env.VITE_STREAM_URL || 'http://192.168.0.101:5000/video_feed',
      updateInterval: parseInt(import.meta.env.VITE_UPDATE_INTERVAL || '2000')
    };
  }

  /**
   * Check if backend is reachable
   */
  async checkConnection(): Promise<boolean> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const response = await fetch(`${this.config.baseUrl}/api/system_status`, {
        method: 'GET',
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      this.isConnected = response.ok;
      return this.isConnected;
    } catch (error) {
      console.warn('Backend connection failed:', error);
      this.isConnected = false;
      return false;
    }
  }

  /**
   * Get current system status
   */
  async getSystemStatus(): Promise<SystemStatus | null> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/system_status`);
      if (!response.ok) throw new Error('Failed to fetch system status');
      
      const data = await response.json();
      return {
        connected: true,
        systemHealth: data.health || 'good',
        uptime: data.uptime || 0,
        version: data.version || '1.0.0'
      };
    } catch (error) {
      console.error('Error fetching system status:', error);
      return null;
    }
  }

  /**
   * Get current telemetry data
   */
  async getTelemetry(): Promise<BotTelemetry | null> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/system_status`);
      if (!response.ok) throw new Error('Failed to fetch telemetry');
      
      const data = await response.json();
      
      return {
        battery: data.battery_level || 85,
        cpuUsage: data.cpu_usage || 0,
        temperature: data.temperature || 45,
        fps: data.camera_fps || 30,
        objectsDetected: data.objects_detected || 0,
        status: data.system_status || 'idle',
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error fetching telemetry:', error);
      return null;
    }
  }

  /**
   * Get current robot location
   */
  async getLocation(): Promise<BotLocation | null> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/slam_map`);
      if (!response.ok) throw new Error('Failed to fetch location');
      
      const data = await response.json();
      
      // Convert SLAM coordinates to GPS coordinates (if available)
      // For demo, use Rajarajeshwari Nagar coordinates with small variations
      const baseLatitude = 12.9134;
      const baseLongitude = 77.5204;
      
      return {
        lat: baseLatitude + (data.current_pose?.x || 0) * 0.0001,
        lng: baseLongitude + (data.current_pose?.y || 0) * 0.0001,
        heading: data.current_pose?.yaw || 0,
        speed: data.velocity || 0,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error fetching location:', error);
      return null;
    }
  }

  /**
   * Get SLAM map data
   */
  async getSlamData(): Promise<SlamData | null> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/slam_map`);
      if (!response.ok) throw new Error('Failed to fetch SLAM data');
      
      const data = await response.json();
      
      return {
        map: data.map_points || [],
        pose: data.current_pose || {x: 0, y: 0, z: 0, roll: 0, pitch: 0, yaw: 0},
        landmarks: data.landmarks || []
      };
    } catch (error) {
      console.error('Error fetching SLAM data:', error);
      return null;
    }
  }

  /**
   * Get voice control status
   */
  async getVoiceStatus(): Promise<VoiceStatus | null> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/voice_status`);
      if (!response.ok) throw new Error('Failed to fetch voice status');
      
      const data = await response.json();
      
      return {
        isListening: data.is_listening || false,
        lastCommand: data.last_command || '',
        language: data.current_language || 'en',
        confidence: data.confidence || 0
      };
    } catch (error) {
      console.error('Error fetching voice status:', error);
      return null;
    }
  }

  /**
   * Send navigation command
   */
  async sendNavigationCommand(command: string, params?: any): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/navigation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          command,
          parameters: params || {}
        })
      });
      
      return response.ok;
    } catch (error) {
      console.error('Error sending navigation command:', error);
      return false;
    }
  }

  /**
   * Emergency stop
   */
  async emergencyStop(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/emergency_stop`, {
        method: 'POST'
      });
      
      return response.ok;
    } catch (error) {
      console.error('Error sending emergency stop:', error);
      return false;
    }
  }

  /**
   * Get video stream URL
   */
  getStreamUrl(): string {
    return this.config.streamUrl;
  }

  /**
   * Get configuration
   */
  getConfig(): ApiConfig {
    return this.config;
  }

  /**
   * Check if currently connected
   */
  isConnectionActive(): boolean {
    return this.isConnected;
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Auto-check connection on startup
apiService.checkConnection().then(connected => {
  console.log(`Backend connection: ${connected ? 'Connected' : 'Offline'}`);
});

export default apiService;