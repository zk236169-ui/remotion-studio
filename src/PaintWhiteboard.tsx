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
import wbData from '../public/current_whiteboard.json';

interface ProScene {
  isShopEnd?: boolean;
  audio: string;
  image?: string;
  frames: number;
  stepTag: string;
  title: string;
  narration: string;
  statBadge?: string;
  motion?: string;
  accent: string;
}

const ProPaintSceneView: React.FC<{
  scene: ProScene;
  index: number;
  total: number;
  shopName: string;
  locationText: string;
  whatsapp: string;
  offerText: string;
}> = ({ scene, index, total, shopName, locationText, whatsapp, offerText }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const p = interpolate(frame, [0, scene.frames], [0, 1], { extrapolateRight: 'clamp' });
  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 140 } });
  const overallPct = ((index + p) / total) * 100;

  // Dynamic cinematic camera motion per scene
  let scale = 1.08;
  let tx = 0;
  let ty = 0;
  if (scene.motion === 'zoom_out') {
    scale = interpolate(p, [0, 1], [1.18, 1.03]);
  } else if (scene.motion === 'pan_left') {
    scale = 1.14;
    tx = interpolate(p, [0, 1], [35, -35]);
  } else if (scene.motion === 'pan_right') {
    scale = 1.14;
    tx = interpolate(p, [0, 1], [-35, 35]);
  } else {
    scale = interpolate(p, [0, 1], [1.03, 1.18]);
    ty = interpolate(p, [0, 1], [12, -12]);
  }

  if (scene.isShopEnd) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#090D16',
          fontFamily: 'Tahoma, Arial, sans-serif',
          direction: 'rtl',
          overflow: 'hidden',
        }}
      >
        {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}
        {scene.image ? (
          <Img
            src={staticFile(scene.image)}
            style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${scale})`,
              opacity: 0.35,
            }}
          />
        ) : null}
        <AbsoluteFill
          style={{
            background: 'linear-gradient(180deg, rgba(9,13,22,0.75) 0%, rgba(9,13,22,0.92) 100%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '60px 44px',
            textAlign: 'center',
          }}
        >
          <div
            style={{
              transform: `scale(${pop})`,
              backgroundColor: 'rgba(15, 23, 42, 0.92)',
              border: `4px solid ${scene.accent}`,
              borderRadius: 34,
              padding: '52px 40px',
              width: '100%',
              boxShadow: '0 30px 70px rgba(0, 0, 0, 0.65)',
            }}
          >
            <div
              style={{
                backgroundColor: scene.accent,
                color: '#FFFFFF',
                fontSize: 30,
                fontWeight: 900,
                padding: '12px 32px',
                borderRadius: 999,
                display: 'inline-block',
                marginBottom: 26,
              }}
            >
              {offerText}
            </div>
            <div style={{ color: '#FFFFFF', fontSize: 66, fontWeight: 900, lineHeight: 1.2, marginBottom: 22 }}>
              {shopName}
            </div>
            <div style={{ color: '#CBD5E1', fontSize: 34, fontWeight: 700, lineHeight: 1.45, marginBottom: 38 }}>
              📍 {locationText}
            </div>
            <div
              style={{
                background: 'linear-gradient(135deg, #16A34A 0%, #15803D 100%)',
                color: '#FFFFFF',
                fontSize: 46,
                fontWeight: 900,
                padding: '24px 48px',
                borderRadius: 24,
                display: 'inline-block',
                boxShadow: '0 16px 38px rgba(22, 163, 74, 0.45)',
                marginBottom: 28,
              }}
            >
              واتساب: {whatsapp}
            </div>
            <div style={{ color: '#F8FAFC', fontSize: 30, fontWeight: 700, lineHeight: 1.45 }}>
              {scene.narration}
            </div>
          </div>
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }

  const words = scene.narration.split(/\s+/).filter(Boolean);
  const activeWordIdx = Math.min(words.length - 1, Math.floor(p * words.length * 1.06));
  const chunkSize = 7;
  const chunkStart = Math.floor(activeWordIdx / chunkSize) * chunkSize;
  const visibleWords = words.slice(chunkStart, chunkStart + chunkSize);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#090D16',
        fontFamily: 'Tahoma, Arial, sans-serif',
        direction: 'rtl',
        overflow: 'hidden',
      }}
    >
      {scene.audio ? <Audio src={staticFile(scene.audio)} /> : null}

      {/* Full-bleed photorealistic scene-matched motion image */}
      {scene.image ? (
        <Img
          src={staticFile(scene.image)}
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
          }}
        />
      ) : null}

      {/* Cinematic top & bottom gradient vignette for razor-sharp Arabic readability */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(180deg, rgba(9,13,22,0.88) 0%, rgba(9,13,22,0.22) 34%, rgba(9,13,22,0.20) 62%, rgba(9,13,22,0.94) 100%)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '74px 48px 92px 48px',
        }}
      >
        {/* Top Hook Header */}
        <div style={{ textAlign: 'center', transform: `scale(${pop})` }}>
          <div
            style={{
              backgroundColor: scene.accent,
              color: '#FFFFFF',
              fontSize: 28,
              fontWeight: 900,
              padding: '10px 30px',
              borderRadius: 999,
              display: 'inline-block',
              marginBottom: 16,
              boxShadow: '0 10px 25px rgba(0,0,0,0.4)',
            }}
          >
            {scene.stepTag}
          </div>
          <div
            style={{
              color: '#FFFFFF',
              fontSize: 52,
              fontWeight: 900,
              lineHeight: 1.25,
              textShadow: '0 4px 18px rgba(0,0,0,0.85)',
            }}
          >
            {scene.title}
          </div>
        </div>

        {/* Bottom Pro Stat Pill + Karaoke Arabic Captions */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 20 }}>
          {scene.statBadge ? (
            <div
              style={{
                backgroundColor: 'rgba(15, 23, 42, 0.88)',
                border: `2px solid ${scene.accent}`,
                color: '#FBBF24',
                fontSize: 28,
                fontWeight: 900,
                padding: '10px 28px',
                borderRadius: 16,
              }}
            >
              ✦ {scene.statBadge}
            </div>
          ) : null}

          <div
            style={{
              width: '100%',
              backgroundColor: 'rgba(9, 13, 22, 0.86)',
              borderBottom: `7px solid ${scene.accent}`,
              borderRadius: 24,
              padding: '28px 32px',
              textAlign: 'center',
              boxShadow: '0 20px 50px rgba(0,0,0,0.55)',
            }}
          >
            <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 14 }}>
              {visibleWords.map((w, localIdx) => {
                const globalIdx = chunkStart + localIdx;
                const isCurrent = globalIdx === activeWordIdx;
                const isSpoken = globalIdx < activeWordIdx;
                return (
                  <span
                    key={globalIdx}
                    style={{
                      fontSize: 42,
                      fontWeight: 900,
                      lineHeight: 1.32,
                      color: isCurrent ? '#FBBF24' : isSpoken ? '#FFFFFF' : 'rgba(255,255,255,0.52)',
                    }}
                  >
                    {w}
                  </span>
                );
              })}
            </div>
          </div>

          <div style={{ color: 'rgba(255,255,255,0.75)', fontSize: 24, fontWeight: 700 }}>
            {shopName} • الرياض
          </div>
        </div>

        {/* Top Progress Bar */}
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 10, backgroundColor: 'rgba(255,255,255,0.18)' }}>
          <div style={{ width: `${overallPct}%`, height: '100%', backgroundColor: scene.accent }} />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const PaintWhiteboard9x16: React.FC = () => {
  const scenes = (wbData.scenes || []) as ProScene[];
  let offset = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: '#090D16' }}>
      {scenes.map((sc, idx) => {
        const from = offset;
        offset += sc.frames;
        return (
          <Sequence key={idx} from={from} durationInFrames={sc.frames}>
            <ProPaintSceneView
              scene={sc}
              index={idx}
              total={scenes.length}
              shopName={wbData.shopName}
              locationText={wbData.locationText}
              whatsapp={wbData.whatsapp}
              offerText={wbData.offerText}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};