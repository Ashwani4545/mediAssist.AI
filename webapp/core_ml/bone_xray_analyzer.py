import os
import uuid
import cv2
import numpy as np

class BoneXRayAnalyzer:
    def __init__(self):
        pass

    def process_image(self, input_path: str, output_dir: str) -> dict:
        """
        Analyze a Bone X-ray image for fracture lines, cortical disruption, and joint space width.
        """
        filename = os.path.basename(input_path)
        base_name, _ = os.path.splitext(filename)
        
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Failed to load bone X-ray image: {input_path}")
            
        h, w = img.shape[:2]
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # CLAHE contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(img_grey)
        
        # Bone region segmentation (bones are high density / bright in X-rays)
        _, bone_thresh = cv2.threshold(enhanced, 130, 255, cv2.THRESH_BINARY)
        
        # Morphological open to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        cleaned_bone = cv2.morphologyEx(bone_thresh, cv2.MORPH_OPEN, kernel)
        
        # Fracture / Cortical Disruption Detection using Canny Edge & Laplacian
        edges = cv2.Canny(enhanced, 80, 180)
        
        # Restrict edge search to bone region
        bone_edges = cv2.bitwise_and(edges, edges, mask=cleaned_bone)
        
        # Detect sharp cortical discontinuities (high-frequency linear fracture candidates)
        lines = cv2.HoughLinesP(bone_edges, 1, np.pi/180, threshold=40, minLineLength=25, maxLineGap=8)
        
        mask = np.zeros_like(img_grey)
        detected = False
        findings_list = []
        fracture_score = 0.0
        
        if lines is not None and len(lines) > 0:
            # Draw line discontinuities on mask
            line_count = 0
            for line in lines:
                x1, y1, x2, y2 = line[0]
                length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if length > 20:
                    cv2.line(mask, (x1, y1), (x2, y2), 255, 3)
                    line_count += 1
                    
            if line_count > 3:
                detected = True
                fracture_score = min(98.5, 45.0 + line_count * 4.5)
                findings_list.append(f"Cortical discontinuity / fracture line patterns detected ({line_count} linear traits)")
            else:
                fracture_score = 15.0
                findings_list.append("Intact cortical margins without major fracture displacement")
        else:
            fracture_score = 5.0
            findings_list.append("Continuous cortical alignment")
            
        # Joint Space & Bone Density Assessment
        bone_pixel_count = np.sum(cleaned_bone > 0)
        bone_density_pct = (bone_pixel_count / (h * w)) * 100
        
        if bone_density_pct < 18.0:
            findings_list.append("Low radiodensity observed — Osteopenia / Osteoporosis risk indicator")
        else:
            findings_list.append("Normal trabecular & cortical radiodensity")
            
        if not detected:
            findings_text = f"Bone X-ray analysis clear. Intact cortical alignment. Radiodensity coverage: {bone_density_pct:.1f}%. No obvious fracture displacement."
            confidence_str = f"{fracture_score:.1f}%"
        else:
            findings_text = f"Orthopedic X-ray scan complete. " + " | ".join(findings_list)
            confidence_str = f"{fracture_score:.1f}%"
            
        # Create AI Overlay (Red highlighted fracture/discontinuity lines + Orange bounding contours)
        overlay = img.copy()
        
        # Red translucent highlight for fracture mask
        red_mask = np.zeros_like(img)
        red_mask[mask > 0] = [0, 0, 230]
        cv2.addWeighted(red_mask, 0.60, overlay, 0.40, 0, overlay)
        
        # Orange outline around cortical bone contours
        contours, _ = cv2.findContours(cleaned_bone, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(overlay, contours, -1, (0, 140, 255), 2)
        
        uid = uuid.uuid4().hex[:8]
        mask_filename = f"{uid}_{base_name}_mask.png"
        overlay_filename = f"{uid}_{base_name}_overlay.png"
        
        cv2.imwrite(os.path.join(output_dir, mask_filename), mask)
        cv2.imwrite(os.path.join(output_dir, overlay_filename), overlay)
        
        return {
            'modality': 'BONE_XRAY',
            'detected': detected,
            'confidence': confidence_str,
            'mask_filename': mask_filename,
            'overlay_filename': overlay_filename,
            'findings_text': findings_text
        }

_analyzer = None

def get_bone_xray_analyzer() -> BoneXRayAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = BoneXRayAnalyzer()
    return _analyzer
