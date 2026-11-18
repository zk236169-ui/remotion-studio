import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import episodeData from '../public/current_episode.json';

interface Beat {
  isShopEnd: boolean;
  visualType: string;
  clip: string;
  audio: string;
  frames: number;
  tag: string;
  headline: string;
  accent: string;
}

const BeatScene: React.FC<{
  beat: Beat;
  index: number;
  totalBeats: number;
  shopName: string;
  locationText: string;
  whatsapp: string;
}> = ({ beat, index, totalBeats, shopName, locationText, whatsapp }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 140, mass: 0.8 },
  });

  const headlineSpring = spring({
    frame: Math.max(0, frame - 4),
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const clipScale = interpolate(frame, [0, beat.frames], [1.0, 1.08], {
    extrapolateRight: 'clamp',
  });

  const progressPct = ((index + Math.min(1, frame / beat.frames)) / totalBeats) * 100;

  // Ending Shop CTA Card (Full Screen Split)
  if (beat.isShopEnd) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#090D16',
          fontFamily: 'Tahoma, Arial, sans-serif',
          direction: 'rtl',
        }}
      >
        <Audio src={staticFile(beat.audio)} />
        {/* Top 55% Shop Front Image with Smooth Zoom */}
        <div style={{ position: 'relative', width: '100%', height: '56%', overflow: 'hidden' }}>
          <Img
            src={staticFile('assets/shop_front.jpg')}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${clipScale})`,
            }}
          />
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(180deg, rgba(9,13,22,0.15) 0%, #090D16 100%)',
            }}
          />
        </div>

        {/* Bottom 44% Clean Contact & Brand Card */}
        <div
          style={{
            flex: 1,
            padding: '24px 56px 64px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            transform: `translateY(${interpolate(enterSpring, [0, 1], [40, 0])}px)`,
            opacity: enterSpring,
          }}
        >
          <div
            style={{
              backgroundColor: beat.accent,
              color: '#052E16',
              fontWeight: 900,
              fontSize: 30,
              padding: '10px 32px',
              borderRadius: 999,
              marginBottom: 22,
              boxShadow: `0 10px 30px ${beat.accent}55`,
            }}
          >
            {beat.tag}
          </div>

          <div
            style={{
              color: '#FFFFFF',
              fontSize: 64,
              fontWeight: 900,
              lineHeight: 1.2,
              marginBottom: 18,
            }}
          >
            {shopName}
          </div>

          <div
            style={{
              color: '#CBD5E1',
              fontSize: 30,
              fontWeight: 600,
              marginBottom: 34,
              lineHeight: 1.4,
            }}
          >
            {locationText}
          </div>

          <div
            style={{
              background: 'linear-gradient(135deg, #16A34A 0%, #15803D 100%)',
              border: '2px solid #4ADE80',
              borderRadius: 24,
              padding: '20px 48px',
              color: '#FFFFFF',
              fontSize: 44,
              fontWeight: 900,
              letterSpacing: 2,
              boxShadow: '0 16px 40px rgba(34,197,94,0.35)',
            }}
          >
            WhatsApp: {whatsapp}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // Standard Scene: Top 30% Sleek Kinetic Broadcast Deck + Bottom 70% Scene-Matched Visual
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#090D16',
        fontFamily: 'Tahoma, Arial, sans-serif',
        direction: 'rtl',
      }}
    >
      <Audio src={staticFile(beat.audio)} />

      {/* TOP 30% STUDIO HEADER DECK (576px) */}
      <div
        style={{
          height: 576,
          width: '100%',
          background: `radial-gradient(circle at 50% 0%, ${beat.accent}28 0%, #0B1120 75%)`,
          borderBottom: `4px solid ${beat.accent}`,
          padding: '54px 52px 36px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          boxSizing: 'border-box',
          position: 'relative',
          zIndex: 10,
        }}
      >
        {/* Top Row: Shop Pill & Scene Counter */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 14,
              backgroundColor: 'rgba(255,255,255,0.07)',
              border: '1px solid rgba(255,255,255,0.14)',
              padding: '10px 24px',
              borderRadius: 999,
            }}
          >
            <div
              style={{
                width: 14,
                height: 14,
                borderRadius: '50%',
                backgroundColor: beat.accent,
                boxShadow: `0 0 14px ${beat.accent}`,
              }}
            />
            <span style={{ color: '#F8FAFC', fontSize: 26, fontWeight: 800 }}>
              {shopName}
            </span>
          </div>

          <div
            style={{
              color: '#94A3B8',
              fontSize: 24,
              fontWeight: 700,
              backgroundColor: 'rgba(15,23,42,0.8)',
              padding: '8px 20px',
              borderRadius: 12,
              border: '1px solid rgba(255,255,255,0.08)',
            }}
          >
            {index + 1} / {totalBeats - 1}
          </div>
        </div>

        {/* Center: Dynamic Accent Tag + Bold Kinetic Arabic Headline */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            gap: 18,
          }}
        >
          <div
            style={{
              backgroundColor: beat.accent,
              color: '#090D16',
              fontSize: 30,
              fontWeight: 900,
              padding: '8px 30px',
              borderRadius: 14,
              transform: `scale(${interpolate(enterSpring, [0, 1], [0.75, 1])})`,
              opacity: enterSpring,
              boxShadow: `0 8px 24px ${beat.accent}44`,
            }}
          >
            {beat.tag}
          </div>

          <div
            style={{
              color: '#FFFFFF',
              fontSize: 58,
              fontWeight: 900,
              lineHeight: 1.25,
              textShadow: '0 6px 24px rgba(0,0,0,0.65)',
              transform: `translateY(${interpolate(headlineSpring, [0, 1], [28, 0])}px)`,
              opacity: headlineSpring,
            }}
          >
            {beat.headline}
          </div>
        </div>

        {/* Bottom: Smooth Episode Progress Bar */}
        <div
          style={{
            width: '100%',
            height: 8,
            backgroundColor: 'rgba(255,255,255,0.1)',
            borderRadius: 999,
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              width: `${progressPct}%`,
              height: '100%',
              backgroundColor: beat.accent,
              borderRadius: 999,
            }}
          />
        </div>
      </div>

      {/* BOTTOM 70% UNOBSTRUCTED SCENE-MATCHED VISUAL (1344px) */}
      <div
        style={{
          height: 1344,
          width: '100%',
          position: 'relative',
          overflow: 'hidden',
          backgroundColor: '#020617',
        }}
      >
        {beat.clip ? (
          <OffthreadVideo
            src={staticFile(beat.clip)}
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${clipScale})`,
            }}
          />
        ) : null}

        {/* Subtle Top/Bottom Vignette for Broadcast Polish */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(180deg, rgba(9,13,22,0.35) 0%, rgba(9,13,22,0) 18%, rgba(9,13,22,0) 82%, rgba(9,13,22,0.65) 100%)',
            pointerEvents: 'none',
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

export const KhyberAnimatedDeckAR: React.FC = () => {
  const beats = episodeData.beats as Beat[];
  let offset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#090D16' }}>
      {beats.map((beat, idx) => {
        const from = offset;
        offset += beat.frames;
        return (
          <Sequence key={idx} from={from} durationInFrames={beat.frames}>
            <BeatScene
              beat={beat}
              index={idx}
              totalBeats={beats.length}
              shopName={episodeData.shopName}
              locationText={episodeData.locationText}
              whatsapp={episodeData.whatsapp}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};