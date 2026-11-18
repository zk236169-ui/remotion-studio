import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
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
  visualStyle: string;
  audio: string;
  frames: number;
  hookTitle: string;
  narrationText: string;
  accent: string;
}

const FullScreenStoryScene: React.FC<{
  beat: Beat;
  index: number;
  totalBeats: number;
  shopName: string;
  locationText: string;
  whatsapp: string;
}> = ({ beat, index, totalBeats, shopName, locationText, whatsapp }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const zoomIn = interpolate(frame, [0, beat.frames], [1.0, 1.14], { extrapolateRight: 'clamp' });
  const pop = spring({ frame, fps, config: { damping: 12, stiffness: 140 } });
  const pulse = Math.sin(frame * 0.15) * 0.08 + 1;

  if (beat.isShopEnd) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#050B14',
          fontFamily: 'Tahoma, Arial, sans-serif',
          direction: 'rtl',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '60px 40px',
          textAlign: 'center',
        }}
      >
        <Audio src={staticFile(beat.audio)} />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            overflow: 'hidden',
            opacity: 0.25,
          }}
        >
          <Img
            src={staticFile('assets/shop_front.jpg')}
            style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoomIn})` }}
          />
        </div>

        <div style={{ position: 'relative', zIndex: 2, maxWidth: 900 }}>
          <div
            style={{
              backgroundColor: beat.accent,
              color: '#052E16',
              fontWeight: 900,
              fontSize: 34,
              padding: '12px 36px',
              borderRadius: 999,
              marginBottom: 26,
              display: 'inline-block',
              boxShadow: `0 12px 35px ${beat.accent}66`,
            }}
          >
            {beat.hookTitle}
          </div>

          <div style={{ color: '#FFFFFF', fontSize: 72, fontWeight: 900, marginBottom: 18, lineHeight: 1.15 }}>
            {shopName}
          </div>

          <div style={{ color: '#94A3B8', fontSize: 32, fontWeight: 700, marginBottom: 40, lineHeight: 1.4 }}>
            {locationText}
          </div>

          <div
            style={{
              background: 'linear-gradient(135deg, #16A34A 0%, #15803D 100%)',
              border: '3px solid #4ADE80',
              borderRadius: 28,
              padding: '24px 54px',
              color: '#FFFFFF',
              fontSize: 48,
              fontWeight: 900,
              letterSpacing: 2,
              boxShadow: '0 20px 50px rgba(34,197,94,0.4)',
              display: 'inline-block',
            }}
          >
            واتساب: {whatsapp}
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // Full-Screen Immersive Visual Metaphor / 3D Simulation Rendering
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#030712',
        fontFamily: 'Tahoma, Arial, sans-serif',
        direction: 'rtl',
        overflow: 'hidden',
      }}
    >
      <Audio src={staticFile(beat.audio)} />

      {/* Full-Screen Dynamic Background Animation / Metaphor */}
      <AbsoluteFill style={{ transform: `scale(${zoomIn})` }}>
        {beat.visualStyle === 'horror_peel' && (
          <div style={{ width: '100%', height: '100%', background: 'radial-gradient(circle at 50% 40%, #450A0A 0%, #030712 85%)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <div style={{ width: 650, height: 650, borderRadius: '50%', background: '#7F1D1D', opacity: 0.35, filter: 'blur(90px)', position: 'absolute' }} />
            <div style={{ transform: `scale(${pop})`, textAlign: 'center', zIndex: 2, padding: '0 50px' }}>
              <div style={{ fontSize: 90, marginBottom: 20 }}>⚠️</div>
              <div style={{ color: '#FCA5A5', fontSize: 55, fontWeight: 900, lineHeight: 1.3, textShadow: '0 10px 30px rgba(0,0,0,0.8)' }}>
                {beat.hookTitle}
              </div>
            </div>
          </div>
        )}

        {beat.visualStyle === 'sun_blister' && (
          <div style={{ width: '100%', height: '100%', background: 'radial-gradient(circle at 50% 30%, #78350F 0%, #030712 85%)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <div style={{ width: 700, height: 700, borderRadius: '50%', background: '#F59E0B', opacity: 0.25 * pulse, filter: 'blur(100px)', position: 'absolute' }} />
            <div style={{ transform: `scale(${pop})`, textAlign: 'center', zIndex: 2, padding: '0 50px' }}>
              <div style={{ fontSize: 90, marginBottom: 20 }}>☀️</div>
              <div style={{ color: '#FDE68A', fontSize: 58, fontWeight: 900, lineHeight: 1.3, textShadow: '0 10px 30px rgba(0,0,0,0.8)' }}>
                {beat.hookTitle}
              </div>
            </div>
          </div>
        )}

        {beat.visualStyle === 'molecular_bond' && (
          <div style={{ width: '100%', height: '100%', background: 'radial-gradient(circle at 50% 40%, #064E3B 0%, #030712 85%)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <div style={{ width: 700, height: 700, borderRadius: '50%', background: '#10B981', opacity: 0.28, filter: 'blur(90px)', position: 'absolute' }} />
            <div style={{ transform: `scale(${pop})`, textAlign: 'center', zIndex: 2, padding: '0 50px' }}>
              <div style={{ fontSize: 90, marginBottom: 20 }}>🛡️</div>
              <div style={{ color: '#A7F3D0', fontSize: 58, fontWeight: 900, lineHeight: 1.3, textShadow: '0 10px 30px rgba(0,0,0,0.8)' }}>
                {beat.hookTitle}
              </div>
            </div>
          </div>
        )}

        {beat.visualStyle === 'color_laser' && (
          <div style={{ width: '100%', height: '100%', background: 'radial-gradient(circle at 50% 40%, #1E1B4B 0%, #030712 85%)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <div style={{ width: 700, height: 700, borderRadius: '50%', background: '#8B5CF6', opacity: 0.3, filter: 'blur(90px)', position: 'absolute' }} />
            <div style={{ transform: `scale(${pop})`, textAlign: 'center', zIndex: 2, padding: '0 50px' }}>
              <div style={{ fontSize: 90, marginBottom: 20 }}>🎨</div>
              <div style={{ color: '#DDD6FE', fontSize: 58, fontWeight: 900, lineHeight: 1.3, textShadow: '0 10px 30px rgba(0,0,0,0.8)' }}>
                {beat.hookTitle}
              </div>
            </div>
          </div>
        )}

        {beat.visualStyle === 'luxury_reveal' && (
          <div style={{ width: '100%', height: '100%', background: 'radial-gradient(circle at 50% 40%, #0C4A6E 0%, #030712 85%)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
            <div style={{ width: 700, height: 700, borderRadius: '50%', background: '#0284C7', opacity: 0.3, filter: 'blur(90px)', position: 'absolute' }} />
            <div style={{ transform: `scale(${pop})`, textAlign: 'center', zIndex: 2, padding: '0 50px' }}>
              <div style={{ fontSize: 90, marginBottom: 20 }}>✨</div>
              <div style={{ color: '#E0F2FE', fontSize: 58, fontWeight: 900, lineHeight: 1.3, textShadow: '0 10px 30px rgba(0,0,0,0.8)' }}>
                {beat.hookTitle}
              </div>
            </div>
          </div>
        )}
      </AbsoluteFill>

      {/* Cinematic Vignette Overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at center, rgba(3,7,18,0) 40%, rgba(3,7,18,0.85) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* Floating Dynamic Subtitle / Narration Box at Bottom */}
      <div
        style={{
          position: 'absolute',
          bottom: 110,
          left: 60,
          right: 60,
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          border: `3px solid ${beat.accent}`,
          borderRadius: 24,
          padding: '30px 36px',
          textAlign: 'center',
          boxShadow: `0 20px 50px rgba(0,0,0,0.7), 0 0 30px ${beat.accent}33`,
          backdropFilter: 'blur(10px)',
        }}
      >
        <div style={{ color: '#FFFFFF', fontSize: 40, fontWeight: 900, lineHeight: 1.35 }}>
          {beat.narrationText}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const KhyberAnimatedDeckAR: React.FC = () => {
  const beats = episodeData.beats as Beat[];
  let offset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#030712' }}>
      {beats.map((beat, idx) => {
        const from = offset;
        offset += beat.frames;
        return (
          <Sequence key={idx} from={from} durationInFrames={beat.frames}>
            <FullScreenStoryScene
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