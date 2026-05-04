import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3-geo';
import { select } from 'd3-selection';
import { drag } from 'd3-drag';
import { zoom } from 'd3-zoom';
import * as topojson from 'topojson-client';
import '../styles/Globe.css';

const GlobeComponent = ({ conflicts, onSelectConflict, selectedConflict }) => {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const [worldData, setWorldData] = useState(null);
  const [tooltipPos, setTooltipPos] = useState(null);
  const [dimensions, setDimensions] = useState({ width: window.innerWidth, height: window.innerHeight });

  const [news, setNews] = useState([]);
  const [loadingNews, setLoadingNews] = useState(false);

  const getIntensityColor = (intensity) => {
    if (intensity >= 8) return 'rgba(220, 38, 38, 0.9)'; // Red
    if (intensity >= 6) return 'rgba(234, 88, 12, 0.9)'; // Orange
    if (intensity >= 4) return 'rgba(245, 158, 11, 0.9)'; // Yellow
    return 'rgba(251, 191, 36, 0.9)'; // Light yellow
  };

  useEffect(() => {
    fetch('https://unpkg.com/world-atlas@2/countries-110m.json')
      .then(res => res.json())
      .then(topology => {
        setWorldData(topojson.feature(topology, topology.objects.countries));
      })
      .catch(err => console.error("Error loading map data:", err));
  }, []);

  useEffect(() => {
    if (selectedConflict) {
      setLoadingNews(true);
      fetch(`http://localhost:5001/api/conflicts/${selectedConflict.id}/news`)
        .then(res => res.json())
        .then(data => {
          setNews(data.articles ? data.articles.slice(0, 3) : []);
        })
        .catch(err => {
          console.error('Error fetching news:', err);
          setNews([]);
        })
        .finally(() => {
          setLoadingNews(false);
        });
    } else {
      setNews([]);
      setTooltipPos(null);
    }
  }, [selectedConflict]);

  useEffect(() => {
    if (!containerRef.current) return;
    const resizeObserver = new ResizeObserver(entries => {
      for (let entry of entries) {
        setDimensions({
          width: Math.max(400, entry.contentRect.width),
          height: Math.max(400, entry.contentRect.height)
        });
      }
    });
    resizeObserver.observe(containerRef.current);
    return () => resizeObserver.disconnect();
  }, []);

  useEffect(() => {
    if (!canvasRef.current || !worldData) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    const { width, height } = dimensions;
    const initialScale = Math.min(width, height) / 2.5;
    
    // Create projection and path
    const projection = d3.geoOrthographic()
      .scale(initialScale)
      .translate([width / 2, height / 2])
      .clipAngle(90)
      .precision(0.5);

    const path = d3.geoPath()
      .projection(projection)
      .context(ctx);

    const drawFrame = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw ocean sphere
      ctx.beginPath();
      path({ type: 'Sphere' });
      ctx.fillStyle = '#eef6fc';
      ctx.fill();

      // Draw land
      ctx.beginPath();
      path(worldData);
      ctx.fillStyle = '#ffffff';
      ctx.fill();
      ctx.lineWidth = 0.5;
      ctx.strokeStyle = '#cddced';
      ctx.stroke();

      // Draw graticule
      ctx.beginPath();
      path(d3.geoGraticule10());
      ctx.lineWidth = 0.3;
      ctx.strokeStyle = 'rgba(200, 215, 230, 0.5)';
      ctx.stroke();

      // Draw sphere outline
      ctx.beginPath();
      path({ type: 'Sphere' });
      ctx.lineWidth = 2;
      ctx.strokeStyle = 'rgba(150, 180, 210, 0.5)';
      ctx.stroke();

      // Draw conflicts
      const rotate = projection.rotate();
      const centerLng = -rotate[0];
      const centerLat = -rotate[1];

      let newTooltipPos = null;

      (conflicts || []).forEach(conflict => {
        // Prevent drawing markers if they are on the back side of the globe
        const dist = d3.geoDistance([conflict.longitude, conflict.latitude], [centerLng, centerLat]);
        if (dist > Math.PI / 2) return; 

        const coords = projection([conflict.longitude, conflict.latitude]);
        if (!coords) return;

        const [x, y] = coords;
        const radius = 6 + (conflict.intensity || 5);
        
        // Draw marker
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, 2 * Math.PI);
        ctx.fillStyle = getIntensityColor(conflict.intensity || 5);
        ctx.fill();
        
        ctx.lineWidth = 2;
        ctx.setLineDash([2, 3]); // Dotted effect
        ctx.strokeStyle = '#000000';
        ctx.stroke();
        ctx.setLineDash([]); // Reset dash

        if (selectedConflict && selectedConflict.id === conflict.id) {
          ctx.beginPath();
          ctx.arc(x, y, radius + 4, 0, 2 * Math.PI);
          ctx.lineWidth = 3;
          ctx.strokeStyle = '#3b82f6';
          ctx.stroke();
          
          newTooltipPos = { x, y };
        }
      });
      
      if (selectedConflict) {
        setTooltipPos(newTooltipPos);
      }
    };

    drawFrame();

    let isInteracting = false;
    let autoRotateVelocity = 0.2;
    let autoRotateTimer;
    let lastTime = performance.now();

    const frameTicker = (time) => {
      if (!isInteracting && !selectedConflict) {
        const dt = time - lastTime;
        const rotate = projection.rotate();
        rotate[0] += (autoRotateVelocity * dt) / 50;
        projection.rotate(rotate);
        drawFrame();
      }
      lastTime = time;
      autoRotateTimer = requestAnimationFrame(frameTicker);
    };

    autoRotateTimer = requestAnimationFrame(frameTicker);

    const customDrag = drag()
      .on('start', () => {
        isInteracting = true;
      })
      .on('drag', (event) => {
        const rotate = projection.rotate();
        const k = 75 / projection.scale();
        projection.rotate([
          rotate[0] + event.dx * k,
          rotate[1] - event.dy * k
        ]);
        drawFrame();
      })
      .on('end', () => {
        isInteracting = false;
      });

    const customZoom = zoom()
      .scaleExtent([0.5, 6])
      .on('start', () => {
        isInteracting = true;
      })
      .on('zoom', (event) => {
        projection.scale(initialScale * event.transform.k);
        drawFrame();
      })
      .on('end', () => {
        isInteracting = false;
      });

    select(canvas)
      .call(customDrag)
      .call(customZoom);

    const handleClick = (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;

      const clickX = (e.clientX - rect.left) * scaleX;
      const clickY = (e.clientY - rect.top) * scaleY;
      
      const rotate = projection.rotate();
      const centerLng = -rotate[0];
      const centerLat = -rotate[1];

      let found = false;
      for (const conflict of (conflicts || [])) {
        // Prevent clicking markers on the back side of the globe
        const dist = d3.geoDistance([conflict.longitude, conflict.latitude], [centerLng, centerLat]);
        if (dist > Math.PI / 2) continue;

        const p = projection([conflict.longitude, conflict.latitude]);
        if (!p) continue;
        
        const [px, py] = p;
        const hitRadius = 8 + (conflict.intensity || 5) + 5;
        
        const dx = clickX - px;
        const dy = clickY - py;
        if (Math.sqrt(dx*dx + dy*dy) <= hitRadius) {
          onSelectConflict(conflict);
          found = true;
          break;
        }
      }
      
      if (!found) {
        onSelectConflict(null);
      }
    };

    canvas.addEventListener('click', handleClick);

    return () => {
      cancelAnimationFrame(autoRotateTimer);
      select(canvas).on('.drag', null);
      select(canvas).on('.zoom', null);
      if (canvas) {
          canvas.removeEventListener('click', handleClick);
      }
    };
  }, [worldData, conflicts, selectedConflict, onSelectConflict, dimensions]);

  let tooltipStyle = { display: 'none' };
  if (tooltipPos && containerRef.current && canvasRef.current) {
    const rect = canvasRef.current.getBoundingClientRect();
    const scaleX = rect.width / dimensions.width;
    const scaleY = rect.height / dimensions.height;
    
    tooltipStyle = {
      position: 'absolute',
      left: tooltipPos.x * scaleX,
      top: tooltipPos.y * scaleY,
      transform: 'translate(calc(-50%), calc(-100% - 20px))', 
      zIndex: 50,
      pointerEvents: 'auto',
      maxWidth: '90vw'
    };
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Recently';
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className='globe-container' ref={containerRef} style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}>
      <canvas
        ref={canvasRef}
        width={dimensions.width}
        height={dimensions.height}
        style={{ display: 'block', width: '100%', height: '100%', cursor: 'grab', touchAction: 'none' }}
      />
      
      {selectedConflict && tooltipPos && (
        <div style={tooltipStyle} className="conflict-speech-bubble">
          <div style={{
            background: 'white',
            borderRadius: '12px',
            padding: '16px',
            boxShadow: '0 8px 30px rgba(0,0,0,0.2)',
            width: '380px',
            maxWidth: '100%',
            maxHeight: '80vh',
            overflowY: 'auto',
            border: '1px solid #e5e7eb',
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute',
              bottom: '-10px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '0',
              height: '0',
              borderLeft: '10px solid transparent',
              borderRight: '10px solid transparent',
              borderTop: '10px solid white'
            }} />
            
            <h3 style={{ margin: '0 0 10px 0', fontSize: '18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              {selectedConflict.name || selectedConflict.title || 'Conflict Details'}
              <button 
                onClick={(e) => { e.stopPropagation(); onSelectConflict(null); }}
                style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '20px', color: '#6b7280', padding: '0', flexShrink: 0, marginLeft: '8px' }}
              >×</button>
            </h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', marginBottom: '15px', fontSize: '13px' }}>
              <div style={{ background: '#f3f4f6', padding: '8px', borderRadius: '6px' }}>
                <strong style={{ display: 'block', color: '#4b5563', fontSize: '12px' }}>Intensity</strong>
                {selectedConflict.intensity || 'N/A'} / 10
              </div>
              <div style={{ background: '#f3f4f6', padding: '8px', borderRadius: '6px' }}>
                <strong style={{ display: 'block', color: '#4b5563', fontSize: '12px' }}>Parties Involved</strong>
                {selectedConflict.parties ? selectedConflict.parties.length : 'N/A'}
              </div>
              <div style={{ background: '#fee2e2', padding: '8px', borderRadius: '6px', gridColumn: '1 / -1' }}>
                <strong style={{ display: 'block', color: '#991b1b', fontSize: '12px' }}>Estimated Deaths</strong>
                {selectedConflict.estimatedDeaths ? selectedConflict.estimatedDeaths.toLocaleString() : 'N/A'}
              </div>
              <div style={{ background: '#fef3c7', padding: '8px', borderRadius: '6px', gridColumn: '1 / -1' }}>
                <strong style={{ display: 'block', color: '#92400e', fontSize: '12px' }}>Status</strong>
                {selectedConflict.status || 'Ongoing'}
              </div>
            </div>

            <div style={{ marginBottom: '15px' }}>
              <strong style={{ display: 'block', marginBottom: '4px', fontSize: '14px' }}>Summary & Involved Parties</strong>
              <p style={{ margin: 0, fontSize: '13px', lineHeight: '1.5', color: '#374151' }}>
                {selectedConflict.description} <br/>
                <strong>Parties:</strong> {selectedConflict.parties && selectedConflict.parties.join(', ')}
              </p>
            </div>

            <div>
              <strong style={{ display: 'block', marginBottom: '8px', fontSize: '14px', borderTop: '1px solid #e5e7eb', paddingTop: '10px' }}>
                Latest News from Trusted Sources
              </strong>
              {loadingNews ? (
                <div style={{ fontSize: '13px', color: '#6b7280' }}>Fetching latest articles...</div>
              ) : news && news.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: '0', listStyle: 'none', fontSize: '13px' }}>
                  {news.map((article, idx) => (
                    <li key={idx} style={{ marginBottom: '8px', paddingBottom: '8px', borderBottom: idx < news.length - 1 ? '1px solid #f3f4f6' : 'none' }}>
                       <a href={article.link} target="_blank" rel="noopener noreferrer" style={{ color: '#2563eb', textDecoration: 'none', fontWeight: '500', display: 'block', marginBottom: '2px' }}>
                         {article.title}
                       </a>
                       <div style={{ fontSize: '11px', color: '#6b7280', display: 'flex', justifyContent: 'space-between' }}>
                         <span>{article.source}</span>
                         <span>{formatDate(article.published)}</span>
                       </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <div style={{ fontSize: '13px', color: '#6b7280' }}>No recent news articles available.</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GlobeComponent;
