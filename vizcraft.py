# AuRA Product Catalog Collector
## Final Field-Survey Upgrade Implementation Prompt

You are acting as a senior full-stack engineer, mobile UX engineer, field-data collection system architect, and QA engineer.

Your task is to MODIFY AND IMPROVE the EXISTING AuRA Product Catalog Collector repository.

This is NOT a greenfield rebuild.

Do NOT throw away working functionality.
Do NOT unnecessarily replace the existing architecture.
Do NOT introduce flashy UI.
Do NOT add unrelated features.
Do NOT use dummy data as a substitute for real functionality.

The current application is already functional and uses:

- React 19
- Vite
- Vanilla CSS/design tokens
- Google Apps Script backend
- Google Drive for image storage
- Google Sheets as the master registry
- Client-side image compression
- Guided camera capture
- Mobile device camera support
- Vercel deployment

Your job is to carefully inspect the existing repository, understand the current workflow, and implement ONLY the approved field-survey improvements described below.

---

# 1. PRIMARY OBJECTIVE

The application is used by field teams visiting agricultural input shops in India to photograph and document agro-input products.

Most actual data collection will happen on MOBILE PHONES.

Therefore the upgraded application must be:

- Mobile-first
- Very fast to operate
- Easy to understand
- Easy to use with one hand where practical
- Responsive on different screen sizes
- Comfortable for repeated product collection
- Resistant to accidental scrolling/jumping
- Suitable for real shops, warehouses and fertilizer stores
- Functional on common Android mobile browsers
- Efficient when users are capturing many products consecutively

Desktop support must remain good, but MOBILE FIELD COLLECTION IS THE PRIMARY UX PRIORITY.

---

# 2. IMPORTANT IMPLEMENTATION RULES

Follow these rules strictly.

## 2.1 Preserve working architecture

Do not rebuild the application unnecessarily.

Keep the existing:

- React/Vite structure
- Google Apps Script integration
- Google Drive submission workflow
- Google Sheet registry
- Image compression pipeline
- Camera/gallery upload support
- submission IDs
- idempotency behavior
- existing sanitization/security behavior
- retry/error handling where already working

Refactor only where required to implement the approved changes cleanly.

---

## 2.2 Do not break existing data collection

Before changing anything:

1. Inspect the current repository.
2. Understand:
   - src/App.jsx
   - src/config.js
   - src/components/GuidedCameraCapture.jsx
   - src/components/UserManualModal.jsx
   - src/utils/compressor.js
   - backend/Code.gs
   - relevant CSS files
3. Trace the complete workflow:
   Category
   → Packaging
   → Product Details
   → Camera
   → Review
   → Submission
   → Google Apps Script
   → Google Drive
   → Google Sheet.

Then implement the upgrades.

---

# 3. APPROVED CHANGE 1
# EXPAND PRODUCT CATEGORIES

The previous broad categories are no longer sufficient.

Implement the following selectable product categories:

1. Fertilizer
2. Fungicide
3. Herbicide
4. Insecticide
5. Micronutrient
6. PGR / Plant Growth Regulator
7. Biostimulant
8. Seed
9. Noise / Negative Sample

Do not hide Fungicide, Herbicide or Insecticide inside one generic "Pesticide" option.

They must be individually selectable because the dataset needs to distinguish them.

Use clear terminology.

Keep the UI concise.

If Marathi labels already exist, maintain the bilingual pattern consistently.

Do not overload category cards with long descriptions on mobile.

---

# 4. APPROVED CHANGE 2
# IMPROVE PRODUCT CATEGORY UI

The current category area is visually crowded.

Redesign the category selection for fast mobile use.

Requirements:

- Large touch targets
- Clearly selected state
- Minimum accidental taps
- Readable on approximately 360px wide screens
- No horizontal scrolling
- Avoid excessive text
- Cards/buttons must wrap intelligently
- Selection should be visually obvious
- Maintain the existing professional green visual identity

Do not create flashy animations.

Use subtle feedback only.

---

# 5. APPROVED CHANGE 3
# ADD BAG / LARGE SACK PACKAGING

The current packaging types are insufficient.

Support at minimum:

1. Bottle / Container
2. Pouch / Packet
3. Bag / Large Sack

Bag / Large Sack is required for products such as:

- fertilizer bags
- large agricultural sacks
- 25 kg bags
- 50 kg bags
- similar large packaging

Do not treat a 50 kg fertilizer bag as a normal pouch.

The packaging type must be stored correctly in:

- frontend state
- submission payload
- Google Drive metadata/folder information where relevant
- Google Sheet registry

Make sure existing records remain compatible.

---

# 6. APPROVED CHANGE 4
# FLEXIBLE PHOTO / ANGLE COLLECTION

The existing fixed angle workflow is too restrictive.

Do NOT hard-code the application around exactly five photos.

Refactor the capture system so photo angles are configuration-driven.

The system must support:

- different number of photos by packaging type
- optional photos
- extra photos when the field agent needs them
- existing Skip Angle functionality
- clear progress tracking
- retake functionality
- review before submission

Preserve the current useful guided workflow.

Do not invent unnecessary agricultural requirements that were not approved.

---

# 7. ADDITIONAL PHOTO CAPTURE

The field team reported that sometimes more views are required than the predefined sequence.

Implement a clean mechanism such as:

"Add Additional Photo"

or equivalent.

Requirements:

- Field agent can capture additional product views after the standard sequence.
- Additional photos must be associated with the same product submission.
- Additional photographs should use stable filenames/tags.
- They must appear in final review.
- They must upload to the same Drive product folder.
- Their count must be reflected correctly.
- They must be distinguishable from the standard required angles.

Example internal tags may be:

Additional_View_01
Additional_View_02
Additional_View_03

Do not impose an unnecessarily small limit unless technically required.

Keep the UX simple.

---

# 8. PACKAGING-SPECIFIC ANGLE CONFIGURATION

Move/maintain angle definitions in a central configuration structure.

Example architectural concept:

PACKAGING_TYPES = {
    bottle: {...angles},
    pouch: {...angles},
    bag: {...angles}
}

Do not scatter angle definitions throughout components.

GuidedCameraCapture should render the required sequence based on configuration.

The implementation should make future changes easy.

The code should not need major component rewrites merely to add another angle later.

---

# 9. APPROVED CHANGE 5
# NPK / FERTILIZER GRADE SUPPORT

The field survey found that fertilizers from the same brand may have different nutrient ratios.

Therefore Brand Name alone is NOT sufficient.

For Fertilizer products, provide a dedicated structured field:

## NPK / Fertilizer Grade

Examples include:

- 19-19-19
- 10-26-26
- 12-32-16
- 18-46-0
- 20-20-0-13
- 0-52-34

Do not automatically infer the NPK ratio from the brand name.

The field user must be able to record the actual grade visible on the package.

Use a user-friendly control.

Preferred behavior:

Common NPK values
+
Other / Custom

If "Other / Custom" is selected, allow manual input.

Do not make uncommon or valid fertilizer grades impossible to enter.

---

# 10. CONDITIONAL PRODUCT FIELDS

Do not show irrelevant fields everywhere.

For example:

If Category = Fertilizer

show:

- Product / Brand Name
- Manufacturer
- Pack Size
- NPK / Fertilizer Grade
- Registration / relevant identification field where currently supported
- Physical Condition
- Notes

For categories where NPK does not apply:

DO NOT show NPK.

The form should dynamically reveal only relevant fields.

Avoid a giant form.

---

# 11. APPROVED CHANGE 6
# PACK SIZE SELECTION

The current Pack Size text field creates unnecessary repetitive typing.

Replace/improve it with a fast structured mobile-friendly selector.

Support common quantities.

Examples:

Volume:
- 50 ml
- 100 ml
- 200 ml
- 250 ml
- 500 ml
- 1 L
- 5 L

Weight:
- 50 g
- 100 g
- 250 g
- 500 g
- 1 kg
- 5 kg
- 10 kg
- 25 kg
- 50 kg

These are examples, not a restriction.

The user must always have:

Other / Custom

for unusual sizes.

A good implementation could use:

Value selector
+
Unit selector

or a clean searchable selection system.

Choose whichever implementation provides the fastest field workflow.

Requirements:

- No cumbersome native dropdown containing dozens of values.
- Must work comfortably on mobile.
- Must allow custom values.
- Existing backend must receive a clean normalized string.

Examples:

250 ml
500 ml
1 L
25 kg
50 kg

---

# 12. APPROVED CHANGE 7
# FIX CAMERA SCROLL / SCREEN-JUMP BUG

This is a HIGH PRIORITY field usability bug.

Current problem:

User opens/captures a photo.

After capture or transition to the next state, the webpage moves vertically/downward.

The field user then has to manually scroll to find the camera/next angle again.

This becomes extremely frustrating when documenting many products.

FIX THIS COMPLETELY.

Expected behavior:

Open Camera
→ Capture Photo
→ Preview
→ Accept/Retake
→ Next Angle

The camera workflow must stay in a predictable viewport.

There must be NO unwanted:

- page jump
- scrolling to bottom
- focus-induced scroll
- layout shift
- automatic browser focus jump

When transitioning between angle states:

Keep the relevant camera section visible.

If programmatic scrolling is required, scroll deliberately to the correct camera container.

Do not scroll the entire page unexpectedly.

Investigate the actual cause.

Possible causes to inspect include:

- element focus
- DOM height changes
- automatic browser scroll
- sticky elements
- modal/container mounting
- image preview dimensions
- conditional rendering
- scrollIntoView()
- button focus
- content expansion
- camera video dimensions

Fix the ROOT CAUSE rather than applying a fragile workaround.

---

# 13. APPROVED CHANGE 8
# SIMPLIFY THE ENTIRE UI

The existing interface is too cluttered during actual field use.

Redesign the experience around progressive disclosure.

Do NOT place every major section in front of the field agent simultaneously.

Recommended interaction model:

STEP 1
Choose Product Category

↓

STEP 2
Choose Packaging Type

↓

STEP 3
Enter Essential Product Information

↓

STEP 4
Capture Photos

↓

STEP 5
Review

↓

STEP 6
Submit

However:

Do not unnecessarily turn this into six disconnected full pages.

The goal is:

LESS CLUTTER
+
FAST FLOW
+
CLEAR PROGRESS

not extra navigation.

Use your UX judgment to build a compact step-based/mobile workflow.

---

# 14. MOBILE-FIRST UX REQUIREMENTS

This project will mostly be used on smartphones.

Treat approximately 360px–430px width as a primary design target.

Test at least:

- 360px width
- 375px width
- 390px width
- 412px width
- 430px width
- tablet
- desktop

Requirements:

## Layout

- Single-column workflow on mobile
- No horizontal overflow
- No text clipped
- No card overflowing screen
- No tiny buttons
- No desktop two-column form forced onto mobile
- Camera should occupy useful viewport area
- Important actions should remain easy to reach

## Touch

Interactive controls should have mobile-friendly touch targets.

Avoid tightly packed small buttons.

## Typography

Maintain current typography/style where possible.

Do not reduce important text until it becomes difficult to read.

## Sticky controls

If using a sticky submit/action bar:

- it must not hide form content
- it must not hide camera controls
- it must respect mobile safe areas
- it must not cause layout jumping
- it must not occupy excessive screen height

Use:

env(safe-area-inset-bottom)

where appropriate.

---

# 15. MOBILE CAMERA EXPERIENCE

Optimize camera capture for Android phones.

Requirements:

- default to rear/environment camera
- preserve existing camera permission handling
- retain gallery upload fallback
- maintain camera flip if currently supported
- camera preview must fit mobile screens
- no accidental zoom/layout overflow
- capture controls should remain reachable
- retake must be easy
- next angle must be obvious
- current angle must be unmistakable
- progress must be visible without excessive UI

Example:

Photo 2 of 6
Back Label

rather than displaying a crowded row of many large angle cards.

On narrow screens, do NOT force all angle tabs onto one row.

Use a compact progress system.

---

# 16. BOTTLE-FIRST OPTIMIZATION

The field survey found that most collected products were bottles.

Therefore optimize the Bottle / Container workflow carefully.

A repeated bottle collection should feel fast:

Category
→ Bottle
→ Details
→ Capture
→ Submit Next Product

Avoid unnecessary taps.

Do not remove information required for dataset quality.

But eliminate redundant interaction.

---

# 17. REVIEW SCREEN

Before submission show a clean summary.

Include:

- category
- packaging
- product name
- manufacturer
- pack size
- NPK if applicable
- condition
- photo count
- standard captured angles
- additional photographs

Images should appear as responsive thumbnails.

Allow:

- Retake
- Remove additional photo where appropriate
- Return to details
- Submit

Avoid giant full-resolution images in the DOM if thumbnails are sufficient.

---

# 18. SUBMISSION VALIDATION

Do not blindly change existing validation.

Currently photography is the primary requirement.

Maintain practical field collection.

At minimum:

- prevent zero-photo product submissions unless Noise workflow intentionally supports its own rules
- validate malformed structured values
- ensure NPK/custom pack size values are correctly serialized
- ensure angle data matches actual uploaded photos

Do not introduce validation that causes field workers to get stuck because a label is unreadable.

The real-world dataset must tolerate incomplete metadata.

Photography is more important than forcing guessed values.

---

# 19. NOISE / NEGATIVE MODE

Do not break the existing Noise / Negative workflow.

When Noise / Negative is selected:

- hide irrelevant product fields
- hide irrelevant packaging controls if current logic requires
- preserve rapid collection behavior if already implemented
- preserve noise tags
- make sure UI redesign does not slow this workflow

---

# 20. BACKEND CHANGES

Update backend/Code.gs only as necessary.

The backend must correctly store the new information.

Update Google Sheet schema to support at minimum:

- Submission ID
- Timestamp
- Category
- Packaging Type
- Product Name
- Manufacturer
- Registration/Certificate Number where applicable
- Pack Size
- NPK / Fertilizer Grade
- Condition
- Angles Captured
- Additional Photo Count if appropriate
- Total Photo Count
- Drive Folder Link
- Notes

Do not corrupt existing rows.

If the registry already exists, implement migration/header handling carefully.

Do not rely on column position blindly if that could damage previous records.

Keep old submissions readable.

---

# 21. GOOGLE DRIVE STORAGE

Keep one logical product submission together.

For example:

Submission Folder
├── Front.jpg
├── Right.jpg
├── Left.jpg
├── Back.jpg
├── Barcode.jpg
├── Additional_View_01.jpg
├── Additional_View_02.jpg
└── ...

Exact filenames should remain consistent with the current submission ID naming convention.

Do not create separate random folders for additional photos.

---

# 22. IMAGE PIPELINE

Preserve existing client-side compression unless testing proves a change is required.

Do not accidentally reduce image quality so much that:

- label text becomes unreadable
- NPK text becomes unreadable
- MRP/batch information becomes unreadable
- barcode becomes unusable
- OCR performance is harmed

Avoid uploading unnecessarily huge original phone images if the current compression pipeline works correctly.

---

# 23. RESPONSIVE UI ARCHITECTURE

Refactor CSS where necessary.

Use sensible breakpoints.

Avoid device-specific hacks.

Prefer:

- CSS Grid
- Flexbox
- clamp()
- min()
- max()
- responsive widths
- CSS variables/design tokens

Avoid hundreds of arbitrary pixel overrides.

Maintain the current professional visual identity.

---

# 24. PERFORMANCE

Field phones may not be premium devices.

Therefore:

- Avoid unnecessary re-renders
- Do not keep multiple huge base64 images rendered unnecessarily
- Revoke temporary object URLs when appropriate
- Clean camera streams properly
- Stop inactive MediaStream tracks
- Avoid memory leaks between product submissions
- Avoid expensive animations
- Keep transitions lightweight
- keep initial page load reasonable

---

# 25. ACCESSIBILITY / FIELD USABILITY

Ensure:

- visible focus states
- adequate contrast
- labels tied to controls
- buttons use meaningful text
- icon-only controls have accessible labels
- disabled buttons visibly appear disabled
- errors are understandable
- mobile keyboard does not cover important controls
- numeric fields use useful input modes where appropriate

---

# 26. ERROR HANDLING

Do not silently fail.

Handle:

- camera permission denied
- camera unavailable
- gallery upload failure
- unsupported file
- image compression failure
- network failure
- Apps Script error
- Drive failure
- duplicate submission retry
- partial upload failure

Messages must be concise and useful.

Do not expose raw stack traces to field users.

---

# 27. DO NOT ADD THESE FEATURES

They are NOT part of this implementation.

Do not add:

- GPS tracking
- shop management
- retailer CRM
- authentication redesign
- barcode auto-identification
- AI product recognition
- OCR autofill
- AI quality scoring
- advanced offline PWA
- analytics dashboard
- maps
- unrelated admin panel
- new database
- unnecessary cloud infrastructure

If the existing system contains some of these capabilities already, do not break them.

But do not expand this task into them.

---

# 28. TEST EVERY WORKFLOW

After implementation, manually test the complete system.

Do not stop after code compilation.

Test:

## Categories

Each category individually.

## Packaging

- Bottle
- Pouch
- Bag / Large Sack

## Fertilizer

Test:

Fertilizer
+
Bag
+
NPK 18-46-0
+
50 kg

and verify the values reach the final backend payload.

Test custom NPK.

## Bottle

Test:

Insecticide
+
Bottle
+
250 ml
+
full camera sequence
+
additional photo
+
review
+
submit.

## Custom pack size

Test a non-standard size.

## Camera

Test:

- Open camera
- Capture
- Retake
- Accept
- Next angle
- Skip
- Additional photo
- Final review

Specifically verify that the page DOES NOT jump down after taking a photo.

## Gallery

Verify uploaded images follow exactly the same state/storage logic as camera images.

## Noise

Verify Noise workflow still works.

## Submission

Verify:

- payload
- Apps Script response
- Drive folder
- image filenames
- Google Sheet entry
- submission ID
- no duplicates after retry

---

# 29. MOBILE TESTING IS MANDATORY

Do not claim completion after testing desktop only.

Use browser responsive/device emulation AND, if a physical Android device is available through the development environment, test on it.

Test especially:

- portrait orientation
- camera capture
- scrolling
- sticky bars
- keyboard opening
- dropdown/select controls
- review screen
- submit workflow

Check for layout shift after camera capture.

---

# 30. NO REGRESSION REQUIREMENT

Before completion verify that these existing features still work:

- existing camera capture
- gallery upload
- compression
- retake
- skip angle
- category selection
- packaging selection
- metadata
- condition selection
- Noise mode
- session/history behavior
- Google Apps Script integration
- Drive upload
- Sheet logging
- submission retry/idempotency
- successful reset for next product

Do NOT sacrifice existing functionality while improving UX.

---

# 31. CODE QUALITY

While implementing:

- remove obvious duplicated logic
- use reusable components where useful
- keep configuration centralized
- use meaningful variable names
- avoid giant conditional JSX blocks where reasonable
- comment only where logic is not self-explanatory
- do not introduce unnecessary dependencies
- do not change dependencies without a concrete need

The result must remain maintainable.

---

# 32. COMPLETION CRITERIA

Do not tell me the task is finished merely because the app builds.

The task is complete only when:

[ ] All 9 categories work

[ ] Bottle / Container works

[ ] Pouch / Packet works

[ ] Bag / Large Sack works

[ ] Fertilizer NPK / Grade works

[ ] Common pack sizes are quickly selectable

[ ] Custom pack sizes work

[ ] Standard photo angles work

[ ] Extra/additional photos work

[ ] Retake works

[ ] Skip works

[ ] Review works

[ ] Camera screen no longer jumps after capture

[ ] UI is significantly less cluttered

[ ] Mobile layout is excellent

[ ] 360px screen works

[ ] 390px screen works

[ ] 430px screen works

[ ] Desktop remains usable

[ ] Google Apps Script accepts new payload

[ ] Google Drive stores all photographs correctly

[ ] Google Sheet stores new metadata correctly

[ ] Existing submissions/backward compatibility are protected

[ ] Noise mode still works

[ ] No major console errors

[ ] No obvious runtime errors

[ ] No broken buttons

[ ] No fake/dummy functionality

---

# 33. WORKING METHOD

Execute the task in this order.

### Phase 1 - Audit

Inspect the existing implementation and understand the current architecture.

Do not modify code before understanding data flow.

### Phase 2 - Plan

Determine exactly which files require modification.

Avoid unnecessary files.

### Phase 3 - Data Model

Update:

- categories
- packaging types
- NPK
- pack size
- photo angle configuration
- additional photos
- payload schema

### Phase 4 - Mobile UX

Simplify the flow and make it mobile-first.

### Phase 5 - Camera

Implement flexible angles and fix the scrolling/layout-jump issue.

### Phase 6 - Backend

Update Google Apps Script and registry schema safely.

### Phase 7 - Integration

Connect everything end-to-end.

### Phase 8 - Testing

Test all workflows and responsive states.

### Phase 9 - Regression Verification

Verify old functionality remains intact.

### Phase 10 - Final Report

Only after everything works, provide a concise implementation report.

---

# 34. IMPORTANT AUTONOMY RULE

Do not repeatedly ask me questions for normal implementation decisions.

Inspect the repository and make sensible engineering decisions yourself.

Ask me only if you encounter a genuine business-rule ambiguity that cannot be safely determined from the existing repository or this specification.

Do NOT stop halfway merely because one issue requires investigation.

Investigate it, fix it, test it, and continue through the remaining phases.

---

# 35. FINAL RESPONSE FORMAT

When implementation is complete, provide:

## 1. Files Modified

List each modified file.

## 2. Features Implemented

Short summary.

## 3. Camera Scroll Bug

Explain:
- root cause
- fix

## 4. Mobile Improvements

Explain major responsive/mobile changes.

## 5. Backend Changes

Explain Sheet/Drive/payload changes.

## 6. Tests Performed

List workflows actually tested.

## 7. Remaining Issues

Only actual unresolved issues.

Do not list imaginary future enhancements.

## 8. Final Verification

Explicitly state which completion checklist items passed and which did not.

---

# FINAL DIRECTIVE

Start by inspecting the current AuRA repository.

Then implement the complete approved field-survey upgrade from beginning to end.

Do not redesign unrelated parts of the product.

Do not stop at analysis.

Do not stop after frontend changes.

Do not stop after writing code.

Do not claim success without testing.

The final result must be a clean, responsive, fast, practical MOBILE-FIRST field data collection application that the AuRA team can actually use while visiting agro-input shops.
