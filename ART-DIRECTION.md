# CCC Website Photography — Art Direction Spec (research-derived)

Derived from peer-reviewed literature on website aesthetics, imagery, and trust.
Applies to ALL site imagery (hero, catalog, lab gallery, future additions).

## The research

1. **First impressions form in ~50 ms and are overwhelmingly visual.**
   Lindgaard, G., Fernandes, G., Dudek, C., & Brown, J. (2006). "Attention web designers: You have 50 milliseconds to make a good first impression!" *Behaviour & Information Technology*, 25(2), 115–126.
   → Every frame must read instantly: one dominant subject, no ambiguity.

2. **Aesthetic perception splits into classical (clean, orderly, symmetrical) and expressive (dramatic, original) dimensions — classical predicts perceived usability/trust.**
   Lavie, T., & Tractinsky, N. (2004). "Assessing dimensions of perceived visual aesthetics of web sites." *Interacting with Computers*, 16(4), 669–705.
   → B2B photography must be CLASSICAL: orderly, symmetric, bright. No moody/dramatic grades (the earlier dark cold-room shot was an expressive move — wrong register for trust).

3. **First-impression appeal is driven by LOW visual complexity and HIGH prototypicality (matching what users expect the category to look like) — prototypicality is the stronger factor.**
   Tuch, A. N., Presslaber, E. E., Stöcklin, M., Opwis, K., & Bargas-Avila, J. A. (2012). "The role of visual complexity and prototypicality regarding first impression of websites." *International Journal of Human-Computer Studies*, 70(11), 826–835.
   → Shoot the *expected* professional photo of each subject. The prototype of "professional lab photo" is bright/white/orderly/close — not unconventional angles or grades.

4. **Imagery that induces social presence (warmth, life) raises perceived trust and appeal.**
   Cyr, D., Head, M., Larios, H., & Pan, B. (2009). "Exploring human images in website design: A multi-method approach." *MIS Quarterly*, 33(3), 539–570.
   → Living green plant material prominent in every frame. Never sterile/empty.

5. **Color maps to brand personality; hue consistency reinforces identity.**
   Labrecque, L. I., & Milne, G. R. (2012). "Exciting red and competent blue: The importance of color in marketing." *Journal of the Academy of Marketing Science*, 40(5), 711–727.
   → One grade across every image: neutral 5000K daylight, high-key, matched color statistics (Reinhard transfer enforced in processing).

## The spec (enforced)

- **S1 · 50ms:** one dominant subject per frame, filling ≥70% frame width
- **S2 · Classical:** straight-on or slight 3/4, symmetric, level, aligned rows, clean surfaces
- **S3 · Prototypical:** bright white-dominant frames, even light, medium-close distance band across the whole set
- **S4 · Presence:** living plant material visible and vigorous in every image
- **S5 · One grade:** statistically matched color (mean/std transfer, target = brightest neutral frame), neutral WB, high-key exposure
- **S6 · Format:** native 3:2 landscape, consistent shallow-focus feel, web export ≤ ~200KB

## Processing pipeline (repeatable)

1. Generate at 2K with the spec embedded in the prompt (explicitly forbidding mood/darkness)
2. Reinhard-style statistical color transfer to the reference frame's mean/std (PIL/numpy)
3. Resize 1400px, JPEG q84
4. Vision QC against S1–S6 + DOM-measured layout checks
