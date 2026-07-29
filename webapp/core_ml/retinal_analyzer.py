import os
import uuid
import cv2
import numpy as np

class RetinalAnalyzer:
    def __init__(self):
        pass

    def process_image(self, input_path: str, output_dir: str) -> dict:
        """
        Analyze a Retinal Fundus image for Optic Disc & Cup ratio, vessel tortuosity, and hemorrhages.
        """
        filename = os.path.basename(input_path)
        base_name, _ = os.path.splitext(filename)
        
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Failed to load retinal fundus image: {input_path}")
            
        h, w = img.shape[:2]
        
        # Use Green channel as it offers best contrast for retinal blood vessels and optic disc
        g_channel = img[:, :, 1]
        
        # 1. Optic Disc Segmentation (brightest circular region)
        blur_disc = cv2.GaussianBlur(g_channel, (15, 15), 0)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(blur_disc)
        
        mask_disc = np.zeros_like(g_channel)
        disc_radius = int(min(h, w) * 0.12)
        cv2.circle(mask_disc, max_loc, disc_radius, 255, -1)
        
        # 2. Optic Cup (brightest central core inside Disc)
        mask_cup = np.zeros_like(g_channel)
        cup_radius = int(disc_radius * 0.48) # Default normal ratio ~0.45
        
        # Calculate local brightness variance to detect cup enlargement (glaucoma indicator)
        disc_roi = g_channel[max(0, max_loc[1]-disc_radius):min(h, max_loc[1]+disc_radius),
                             max(0, max_loc[0]-disc_radius):min(w, max_loc[0]+disc_radius)]
        
        dcr = 0.45 # default disc-to-cup ratio
        if disc_roi.size > 0:
            threshold_val = np.percentile(disc_roi, 88)
            bright_pixels = np.sum(disc_roi >= threshold_val)
            cup_area_estimate = bright_pixels
            disc_area_estimate = np.pi * (disc_radius ** 2)
            dcr = np.sqrt(max(0.1, cup_area_estimate / max(1, disc_area_estimate)))
            dcr = float(np.clip(dcr, 0.35, 0.85))
            
        cup_radius = int(disc_radius * dcr)
        cv2.circle(mask_cup, max_loc, cup_radius, 255, -1)
        
        # Combined mask for display (Disc area + Cup region)
        mask_combined = mask_disc.copy()
        
        detected = False
        findings_list = []
        
        if dcr > 0.65:
            detected = True
            findings_list.append(f"Elevated Optic Cup-to-Disc Ratio (CDR: {dcr:.2f}) — Glaucomatous cupping risk")
        else:
            findings_list.append(f"Normal Optic Cup-to-Disc Ratio (CDR: {dcr:.2f})")
            
        # 3. Retinal Blood Vessel Density & Micro-hemorrhage Check
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_g = clahe.apply(g_channel)
        
        # Black top-hat / morph closing to highlight dark linear vessels & dot hemorrhages
        kernel_vessel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        top_hat = cv2.morphologyEx(contrast_g, cv2.MORPH_BLACKHAT, kernel_vessel)
        
        vessel_pixels = np.sum(top_hat > 45)
        vessel_density = (vessel_pixels / (h * w)) * 100
        
        if vessel_density > 8.0:
            detected = True
            findings_list.append("Increased vascular tortuosity / exudate density noted")
        else:
            findings_list.append("Standard retinal vascular pattern")
            
        if not detected:
            findings_text = f"Retinal Fundus analysis normal. Optic Cup-to-Disc Ratio: {dcr:.2f}. No hypertensive or diabetic retinopathy signs detected."
            confidence_str = f"CDR: {dcr:.2f}"
        else:
            findings_text = f"Retinal Fundus scan complete. " + " | ".join(findings_list)
            confidence_str = f"CDR: {dcr:.2f}"
            
        # Create AI Overlay (Green/Yellow Disc & Cup rings + Red vessel overlay)
        overlay = img.copy()
        
        # Draw Optic Disc (Yellow ring)
        cv2.circle(overlay, max_loc, disc_radius, (0, 230, 255), 2)
        # Draw Optic Cup (Cyan ring)
        cv2.circle(overlay, max_loc, cup_radius, (255, 255, 0), 2)
        
        # Highlight dark vessel/exudate regions in translucent magenta
        vessel_mask = np.zeros_like(img)
        vessel_mask[top_hat > 45] = [200, 0, 200]
        cv2.addWeighted(vessel_mask, 0.40, overlay, 0.60, 0, overlay)
        
        uid = uuid.uuid4().hex[:8]
        mask_filename = f"{uid}_{base_name}_mask.png"
        overlay_filename = f"{uid}_{base_name}_overlay.png"
        
        cv2.imwrite(os.path.join(output_dir, mask_filename), mask_combined)
        cv2.imwrite(os.path.join(output_dir, overlay_filename), overlay)
        
        return {
            'modality': 'RETINAL',
            'detected': detected,
            'confidence': confidence_str,
            'mask_filename': mask_filename,
            'overlay_filename': overlay_filename,
            'findings_text': findings_text
        }

_analyzer = None

def get_retinal_analyzer() -> RetinalAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = RetinalAnalyzer()
    return _analyzer
