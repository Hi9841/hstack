---
name: audit-animations
description: Audit and fix UI motion in an app against 7 practical animation rules - press feedback, entry scale, tooltip delay, easing, transform origin, duration, and blur. Use when the user asks to audit, review, polish, or fix animations, transitions, or the feel of a UI across an app or component set.
---

# Audit Animations

Find each UI motion violation in the app, fix it, and prove the fix in the running app. The only done-condition is the report in step 8, with each rule accounted for.


## Workflow

1. Identify the UI stack: CSS, Tailwind, Motion, Radix, Base UI, or a native toolkit. If the stack is not CSS, apply the same values with the equivalent API.
2. Find the shared easing and duration tokens. If there are no tokens, add them in one location.
3. Make a list of all interactive and animated components: buttons, tooltips, popovers, dropdowns, selects, dialogs, spinners, toasts, and lists.
4. Search for these patterns: `scale(0)`, `scale-0`, `scale: 0`, `ease-in`, `transition: all`, `transition-all`, `transform-origin`, `origin-center`, `:active`, `active:scale`, `duration-`, `delayDuration`, `skipDelayDuration`, `data-instant`, `@keyframes`.
5. Examine each component in the list against each rule. A component can violate a rule with no matching pattern, so the search results are not the full audit.
6. Fix the violations in shared components first. Then fix the remaining local styles.
7. Run the real app and operate each changed component. Slow the animations by 2-5x to examine timing and origin. Then run the lint and type checks of the repo.
8. Write the report.

## Rules

1. Scale your buttons.
   - Each pressable element scales to 0.97 on `:active`, with `transition: transform 160ms ease-out`.
   - Disabled elements do not scale.
   - Each user action gives immediate feedback. A form submit shows a loading state. A copy action shows a success state.

2. Do not animate from `scale(0)`.
   - Entry animations start at scale 0.9 or higher, with `opacity: 0`. Use 0.93 as the default.

3. Do not delay subsequent tooltips.
   - The first tooltip in a group has a delay.
   - When a tooltip is open, the next tooltip in the group opens with no delay and no animation.
   - In Radix, set `skipDelayDuration` on the provider.
   - In Base UI, set `transition-duration: 0ms` on `[data-instant]`.

4. Choose the right easing.
   - Elements that enter or exit the screen use ease-out.
   - Do not use `ease-in` on UI animation.
   - Do not use the built-in CSS curves. Use custom curves from the shared tokens.
   - Default ease-out: `cubic-bezier(0.23, 1, 0.32, 1)`.
   - Default ease-in-out for movement on the screen: `cubic-bezier(0.77, 0, 0.175, 1)`.

5. Make animations origin-aware.
   - Popovers, dropdowns, selects, and tooltips scale from the trigger, not from the center.
   - In Base UI, use `transform-origin: var(--transform-origin)`.
   - In Radix, use the variable of the component, for example `var(--radix-dropdown-menu-content-transform-origin)`.
   - Modals have no trigger anchor, so modals stay centered.

6. Keep animations fast.
   - UI animations stay under 300ms. Use approximately 180ms for selects and dropdowns.
   - Spinners turn fast, because a fast spinner makes the load seem shorter.
   - Remove animation and hover effects from items that users see tens or hundreds of times each day.
   - Do not animate actions that start from the keyboard.

7. Use blur when nothing else works.
   - First try different easings and durations on a crossfade that looks wrong.
   - If the crossfade still looks wrong, add `filter: blur(2px)` during the transition.
   - Do not add blur to all transitions. Use it only on a crossfade that needs it.

## Limits

- Change only motion and press feedback. Do not change layout, color, or copy.
- Animate only `transform`, `opacity`, and `filter` where possible. Replace `transition: all` with the exact properties.
- Keep the `prefers-reduced-motion` behavior. If it is missing, add it. Remove movement and keep fades.
- If a violation is intentional, keep it and give the reason in the report.

## Report

Give one table for each rule, with the columns: Location | Before | After | Why.
If a rule has no violations, write "Pass" and give the components that you examined.
At the end, give these items:

- The components that you operated in the real app
- The lint and type check results
- The items that you did not verify
