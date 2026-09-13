---
name: image-prompts
description: Use this skill whenever writing or revising the prompt text in a Tyrnarra art spec (`<slug>.set.json`) - the `character`, `wardrobe` and `framing` fields that feed Midjourney, fal.ai and the local renderer. Trigger on "write the art spec for [NPC]", "the render ignored [detail]", "this prompt is too long", "fix the prompt", the art step of building a quest cast (quest-workflow Phase 7.4), or before invoking npc-art. Optimised for Midjourney, which is the primary pipeline. Do not use for lore prose, page copy, or the mechanics of running the renderers (that is npc-art and tools/imageGen/README.md).
---

# image-prompts

How to write the prompt text in a `<slug>.set.json`. The renderers are covered
elsewhere (`tools/imageGen/README.md`); this is about the words.

One spec feeds all three tiers, so it is written for the strictest reader:
**Midjourney**, the primary pipeline as of 2026-09-13.

---

## The one rule

**Write only what a camera could photograph.**

An image model renders what it can see. It cannot render history, intention,
reputation, or irony, and every word spent on those is a word not spent on the
image. This single test settles most questions:

> Could a stranger, looking only at the finished picture, point at the thing
> this phrase describes?

If no, cut it or convert it.

---

## Convert, do not simply delete

Interiority is usually load-bearing: it is *why* the character looks the way
they do. Keep the look, drop the explanation.

| Written as | Rendered as |
|---|---|
| "he is a man managing his own face" | "a practised smile that does not reach his eyes" |
| "worry shows only at the edges" | "tight skin around the eyes, dark circles beneath" |
| "dressed above his station" | "every piece immaculate and slightly too formal for the wearer" |
| "three weeks underfed and running on pure temper" | "gaunt, hollow-cheeked, jaw set, eyes hard" |
| "unnervingly calm" | "expression mild and still, gaze level" |

The right-hand column is not a loss of character. It is the same character,
described by someone who can only look at him.

---

## Do not use invented setting vocabulary

The model has never read the lore. A name from Tyrnarra is not a description,
it is an unknown token, and it either does nothing or pulls toward something
unrelated that happens to sound similar.

- **Cut:** Emarrean, Sortalde, Fenurran, Vindul, Zuzental, any kingdom, domain,
  house, order or god name. Also cut the *fact* of the reference: "the court
  fashion he saw exactly once" is backstory, not appearance.
- **Keep:** vocabulary the model demonstrably knows. Real-world mythology and
  common fantasy ancestries are fine and often efficient: *kitsune* reliably
  produces the right creature and saves a dozen words; so do *halfling*, *orc*,
  *minotaur*, *tengu*.
- **Describe, then optionally name:** for anything niche, lead with the visual
  and let the name ride along. *Vishkanya* alone is a gamble; "fine jewel-toned
  scaling across the temples and the backs of the hands" is not.

The test: **would this word mean anything to someone who has never seen your
setting?** If it only works because *you* know what it means, it is not
working.

---

## Describe the face, do not appraise the expression

"A practised courteous smile that does not reach his eyes" passes the camera
test and still failed: Midjourney rendered a warm open grin. The phrase is a
**judgement about** a smile, not a description of one, so the model had to guess
what it looks like and guessed wrong.

Name the muscles instead. What that sentence was reaching for was:

> A wide warm open smile, cheeks lifted, the easy smile of a habitually
> cheerful man. Above it his eyebrows are raised and drawn hard together at the
> inner ends, deeply creasing the middle of his forehead, and his eyes are wide
> and frightened, glassy and unsteady.

The mask reads as a mask because the **features are given contradictory
instructions**. That contradiction is the whole effect, and it has to be stated,
because "does not reach his eyes" only carries it for a reader who already knows
the idiom.

**Work out which feature actually carries the tell.** Two drafts of this failed
by weakening the smile: "a smile that does not reach his eyes", then "a small
closed-mouth smile, the lips pressed and strained". Both were wrong about the
character. Harlen is a cheerful man *trying to be cheerful*, so the smile is
wide and genuine and the fear is entirely above it, in the eyes and harder still
in the brow. Weakening the mouth produced a man who was visibly not-smiling,
which is a different person.

Ask the author which feature betrays him and which feature is doing its job. Do
not assume the tell is spread evenly across the face; it usually is not.

Same trap in a different coat: *composed*, *guarded*, *haunted*, *steely*,
*kind-faced*. Each is a conclusion a viewer draws. Give the features that make
them draw it.

---

## The `negative` field: use it almost never

A spec may carry `negative`, which reaches Midjourney as `--no`. **The default
is to have none.** Both specs that were given one had it removed again within
the hour, each time because the flag was fighting something the prompt wanted.
Reach for it only when a specific failure has repeated across several renders
and no positive phrasing has moved it, and expect to delete it once an anchor
exists.

It is a blunt instrument: `--no` suppresses a **concept**, not the excess of a
concept, and it cannot tell the difference between the version you hate and the
version you want.

A list written to curb a too-cheerful Harlen (`grin, broad smile, cheerful,
jolly`) removed his smile altogether, because every one of those entries carries
*smile* with it and he needed one. The test before adding an entry:

> If the model took this word completely away, would the image still be right?

If the thing you want is a *small* version of the thing you are excluding, the
flag is the wrong tool. Say the small version in the prompt and leave `--no`
empty.

### A defence belongs to the anchor, never to a ref shot

Aldous kept rendering as a skeleton, so his spec grew defences: "full soft
flesh", "intact lips and nose", "living skin", and the word *living* in all
three framings. That was correct for text-to-image and **actively wrong once an
anchor existed.** A ref shot's framing is its entire prompt, so with the face
already carried by the attached image, the whole instruction became "living man,
fully fleshed" and Midjourney obliged: an ordinary healthy butler, the uncanny
gone.

The `--no` went the same way. `skeleton, corpse, undead` was right while the
model was inventing him from words, and wrong once it was copying a face:
suppressing *undead* and *corpse* strips the deathliness that makes him work.
His spec now carries no negative at all.

The rule: **a defence protects the shot that has nothing else to go on.** It
belongs to a text-to-image anchor and nowhere else. Once an anchor exists and is
attached, drop the defensive wording from the framings and drop the `negative`
field. What makes Aldous wrong is the stillness and the empty courtesy, not a
reminder that he has skin.

Check for this whenever a spec has been fought with. The wording that won the
text-to-image battle tends to migrate into the framings and the negative, where
it is dead weight at best and, once a reference is doing the work, a straight
instruction to undo the thing you wanted.

---

## Prose rules

- **No em-dashes.** House rule everywhere in this project, prompts included. A
  comma, colon, semicolon or full stop always serves.
- **No keyword soup.** "masterpiece, 8k, trending, ultra detailed" actively
  degrades modern Midjourney. Write plain descriptive sentences.
- **Concrete over vague.** "a woman" is nothing; "a woman in her forties,
  broad-shouldered, close-cropped grey hair, a burn scar along one forearm" is
  something. Prefer nouns and observable traits to adjectives of quality.
- **Say it once.** Repeating a trait does not strengthen it, it just spends
  budget.

---

## When the words will not carry it, render the anchor elsewhere

Some faces do not survive a text prompt. Harlen is a cheerful man in terror, and
Midjourney would not produce it: not from a long description, not from a short
one, not from `/describe` fed its own successful reference. Local FLUX got it on
the first attempt.

**The fix is not to give up on the primary renderer.** Render the *anchor*
wherever the expression actually works, then attach it as the reference and let
the primary renderer do the rest of the set. Midjourney could not invent that
face, but it carried it faithfully into a portrait and a scene, matching the
brow, the eyes and the smile.

This is why the anchor matters more than the other shots and why it is worth
spending a different renderer on. Record which renderer made what in the spec's
`render` block, so a later session extending the set knows where to go back to.

Before reaching for this: a subtle expression may also be getting smoothed away
by Midjourney's aesthetic pull. Low `--stylize` and dropping `--profile` are
worth one test each, since both bias toward a pleasant face.

---

## The three fields

| Field | Holds | Test |
|---|---|---|
| `character` | The body: ancestry, age, build, colouring, face, hair, visible marks, and the expression as an observer reads it. | Nothing here should change between shots. |
| `wardrobe` | The garments as seen: cut, fabric, colour, condition, ornament. | Nothing about where it came from or what it cost. |
| `framing` | The camera: shot type, crop, angle, pose, and for a scene shot the setting and action. | This is the only field that differs per shot. |

Keep them in their lanes. A `character` field that describes a coat, or a
`framing` that re-describes the face, means the same words get sent twice.

---

## Length: shorter is not a compromise, it is the technique

**Every word competes with every other word.** Midjourney weights the whole
prompt, so a detail described at length does not come out stronger, it comes out
sharing the frame with everything else you said. Harlen's anchor ran 142 words,
of which the face was about fifteen percent and the brocade rather more; he
rendered barely worried. The same face in three short sentences, in a 58-word
prompt, is a third of the prompt instead of a seventh.

> A beaming wide smile. Frightened eyes. Eyebrows raised and pinched together.

**Aim for 50 to 70 words on an anchor**, not 150. Short sentences, one feature
each, so nothing is buried in a subordinate clause. Trust the model on anything
it already knows how to draw: it does not need to be told that curls are tidy
and combed and neat, and a coat does not need its buttons counted.

The 150-word figure is a **warning line, not a target** (measured: 148 clean,
152 warns). The server reports `words` per shot and flags `long`. Being far
under it is the goal, not a near miss of it.

**What to cut first**, in order: wardrobe detail that will be a few pixels wide
in the shot, adjectives stacked on one noun, anything the framing already says,
and any clause explaining a thing already shown.

- **Anchor shot** (the text-to-image full body) carries `character` + `wardrobe`
  + `framing`, so it is the long one and the one to keep lean. Trim `character`
  and `wardrobe` first: they are shared by every shot, so the trim pays three
  times.
- **Ref shots** (portrait, scene) send **framing only**. The attached anchor
  carries identity, so the description is redundant there. This is handled by
  the server, not by you: do not hand-write identity back into a `framing`.

---

## Worked example: Harlen Doss

**Before** (`character`, 97 words):

> A halfling man in his forties, short and stocky with the sturdy build and
> proportions of his people, standing about four feet tall, neat and carefully
> groomed with tidy brown curls. His expression is composed and professionally
> pleasant, a merchant's practised courteous smile held firmly in place: he is a
> man managing his own face. The worry shows only at the edges, in the tightness
> around his eyes and the dark circles under them, and in the way his hands are
> held a little too still. Calm, controlled, mask firmly on

Three problems. *"the sturdy build and proportions of his people"* says nothing
a camera sees that "short and stocky" has not already said. *"he is a man
managing his own face"* and *"mask firmly on"* are the author explaining the
character to the reader. *"The worry shows only at the edges"* narrates a
visual instead of giving it.

**After** (52 words), every visible signal kept:

> A halfling man in his forties, about four feet tall, short and stocky, broad
> through the shoulders. Tidy brown curls, neatly groomed, clean-shaven. A
> practised courteous smile that does not reach his eyes, tight skin at the
> corners, dark circles beneath. Hands held very still, clasped in front of him.

**Before** (`wardrobe`, opening):

> dressed considerably above his station in the Emarrean court fashion he saw
> exactly once: a long deep wine-red coat …

**After:**

> A long deep wine-red coat …

The setting name and the anecdote both go. What replaces them is nothing: the
garments were already described, and *"immaculate and slightly too formal for
the wearer"* at the end carries the whole point of the outfit in seven words a
camera can see.

---

## Before you hand a spec to a renderer

1. Read each field aloud and ask the camera question of every clause.
2. Search for setting vocabulary and for backstory verbs ("had", "once",
   "used to", "remembers", "imitating").
3. Check for em-dashes.
4. Check the anchor's word count against ~150.
5. Confirm `character` holds no clothing and `framing` holds no identity.
