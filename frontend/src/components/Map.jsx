import { useState, useEffect, useMemo } from 'react';
import { GoogleMap, Marker, InfoWindow, useLoadScript } from '@react-google-maps/api';
import { initializeApp } from 'firebase/app';
import { getDatabase, ref, onValue } from 'firebase/database';

const firebaseConfig = {
  apiKey: 'AIzaSyCZysurVDWGzvNIW9zVPpuK68K7X9vsrz4',
  authDomain: 'location-27eb2.firebaseapp.com',
  databaseURL: 'https://location-27eb2-default-rtdb.firebaseio.com',
  projectId: 'location-27eb2',
  storageBucket: 'location-27eb2.firebasestorage.app',
  messagingSenderId: '1009549401362',
  appId: '1:1009549401362:web:e87320c483ad853cd2e7cb',
  measurementId: 'G-1Z9Q3E3HTE'
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

export default function Map() {
  const { isLoaded } = useLoadScript({ googleMapsApiKey: import.meta.env.VITE_GMAP_KEY });

  const [pos, setPos] = useState(null);         // {lat, long}
  const [addr, setAddr] = useState(null);       // formatted_address
  const [showInfo, setShowInfo] = useState(false);
  const [fall, setFall] = useState(null);       // {ts, fall}

  /* ── live coordinates ── */
  useEffect(() => onValue(ref(db, 'location'), s => setPos(s.val())), []);

  /* ── reverse‑geocode ── */
  useEffect(() => {
    if (!pos) return;
    (async () => {
      const url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${pos.lat},${pos.long}&key=${import.meta.env.VITE_GMAP_KEY}`;
      try {
        const d = await (await fetch(url)).json();
        setAddr(d.status === 'OK' ? d.results[0].formatted_address : 'Unknown');
      } catch {
        setAddr('Error');
      }
    })();
  }, [pos]);

  /* ── latest fall ── */
  useEffect(
    () =>
      onValue(ref(db, 'falls'), snap => {
        const v = snap.val();
        if (!v) return setFall(null);
        const latest = Object.values(v).sort((a, b) => new Date(b.ts) - new Date(a.ts))[0];
        setFall(latest);
      }),
    []
  );

  const position = pos
    ? { lat: parseFloat(pos.lat), lng: parseFloat(pos.long) }
    : { lat: 12.9716, lng: 77.5946 };

  const fallCard = useMemo(() => {
    if (!fall || !fall.fall) return null;
    const dt = new Date(fall.ts).toLocaleString();
    return (
      <div className="mt-6 p-4 rounded-lg bg-red-50 border border-red-400">
        <div className="text-red-700 font-semibold mb-1">Fall Detected</div>
        <div className="text-sm text-red-600">Last event: {dt}</div>
        <button
          className="mt-4 w-full py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
          onClick={() => setShowInfo(true)}
        >
          View on Map
        </button>
      </div>
    );
  }, [fall]);

  if (!isLoaded) return <div className="text-center mt-20 text-xl">Loading map…</div>;

  return (
    <div className="h-screen w-screen flex flex-col bg-gray-100">
      <header className="p-4 text-center text-2xl font-semibold bg-blue-600 text-white shadow">
        Parental Dashboard
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1">
          <GoogleMap
            zoom={15}
            center={position}
            mapContainerClassName="h-full w-full"
            onClick={() => setShowInfo(false)}
          >
            <Marker position={position} onClick={() => setShowInfo(true)} />
            {showInfo && (
              <InfoWindow position={position} onCloseClick={() => setShowInfo(false)}>
                <div className="text-sm">
                  <div className="font-semibold mb-1">Current Location</div>
                  <div>{addr || 'Fetching address…'}</div>
                  <div className="mt-2">
                    Lat: {position.lat.toFixed(5)} <br />
                    Lng: {position.lng.toFixed(5)}
                  </div>
                </div>
              </InfoWindow>
            )}
          </GoogleMap>
        </div>

        <aside className="w-96 bg-white p-6 shadow-inner border-l overflow-y-auto">
          <h2 className="text-xl font-semibold mb-4">Location Details</h2>
          <div className="space-y-2 text-gray-700">
            <div>
              <span className="font-medium">Latitude:</span> {position.lat}
            </div>
            <div>
              <span className="font-medium">Longitude:</span> {position.lng}
            </div>
            <div>
              <span className="font-medium">Address:</span>
              <br />
              {addr || 'Fetching address…'}
            </div>
            {fallCard}
          </div>
        </aside>
      </div>
    </div>
  );
}
