# What kind of continuity does Jāmbavant carry?

The strongest reading from these passages is **continuity through remembered deeds and recognition**, rather than longevity alone. But recognition is not automatic: the Kṛṣṇa encounter begins with a mistake. This is an interpretation of selected translations, not a claim about textual development or authorial intention.

## First, audit the algorithm's three conflicts

The MWIS experiment suppresses direction and relationship type. Its rule that two selected records cannot share a neighbor makes the following very different relationships equivalent as optimization conflicts:

| Selected record | Actual shortest path | Passage evidence | What it supports |
|---|---|---|---|
| Rāma | Jāmbavant → Rāma | RMW_017; Rāmāyaṇa 6.27.10–14 | Participation in Rāma's allied army |
| Satrājita | Jāmbavant → Kṛṣṇa ← Satrājita | GYM279; JV012–014, JV016; JV035 | Different roles in the jewel narrative: opponent and recognizer, versus accuser |
| Bali, the Daitya | Jāmbavant → Indra ← Bali | RMW_030; SB8P067 | One assists Indra, the other fights Indra; the passages do not establish the same battle |

The arrows in this table indicate claim direction, not identical meanings. The [machine-readable audit](mwis-path-audit.json) retains every claim, predicate, speaker and source on every shortest path. Reproduce it with `python analyze_jambavant_paths.py`; it uses the graph at `d966449`, before the new recognition-state claim below.

The Bali path needs particular care. [Rāmāyaṇa 6.27.12](https://sanskritdocuments.org/sites/valmikiramayan/yuddha/sarga27/yuddharoman27.htm) attributes Jāmbavant's help to Indra in a gods–demons battle; [Bhāgavata 8.10.28](https://vedabase.io/en/library/sb/8/10/28/) pairs Bali against Indra. A shared participant does not establish that Jāmbavant fought Bali. The Bali record also incorporates the repository's cross-text alignment of the Ādiparvan dossier with the Bhāgavata figure.

## 1. Memory gives his present counsel a larger frame

In [Rāmāyaṇa 4.65.10–17](https://www.valmikiramayan.net/utf8/kish/sarga65/kishkindhasans65.htm), Jāmbavant contrasts earlier prowess with present limitations and recalls circling Trivikrama at Bali's sacrifice. This places a cosmic episode inside the immediate discussion of who can cross the ocean.

**Reading:** remembered participation supplies a perspective on present capability. The scene makes experience narratively useful even when physical capacity has declined. It does not expressly say that everyone accepts his advice because he witnessed Trivikrama.

This recollection provides a literary route to the Bali/Vāmana world that is distinct from the algorithm's shorter route through Indra. [Bhāgavata 8.21.8](https://vedabase.io/en/library/sb/8/21/8/) separately depicts Jāmbavant proclaiming Vāmana's victory. The actions and textual contexts remain distinct.

## 2. The experienced recognizer first fails to recognize

The cave encounter is not immediate reunion. [Bhāgavata 10.56.21](https://vedabase.io/en/library/sb/10/56/21/) has the nurse's frightened cry bring Jāmbavant running. In [10.56.22](https://vedabase.io/en/library/sb/10/56/22/), the narrator explicitly says that he takes Kṛṣṇa for an ordinary person and fights without understanding his status. Only later does he identify his opponent as Viṣṇu in [10.56.26](https://vedabase.io/en/library/sb/10/56/26/).

**Reading:** the narrative stages recognition as a change in understanding. His earlier experience does not give him infallible knowledge of a new encounter. This makes his recognition more consequential than simply having the same long-lived character appear in another story.

The new graph claim **JV037**, `initially_mistakes_for_ordinary_person`, records the narrator's account at 10.56.22. It complements JV013's later `recognizes_as_vishnu`. Neither becomes an objective identity assertion. The two claims concern different moments, so their coexistence is not a contradiction.

## 3. Recognition explicitly brings the Laṅkā story into the Kṛṣṇa encounter

In [Bhāgavata 10.56.28](https://vedabase.io/en/library/sb/10/56/28/), Jāmbavant addresses Kṛṣṇa through the ocean crossing, bridge, Laṅkā and Rāvaṇa episode. Rāma is not named in this verse; identifying the referenced narrative is contextual.

**Reading:** the continuity is spoken within the scene, rather than resting solely on our decision to merge identically named records. It interprets the present opponent through earlier divine deeds. The verse does not itself claim that Jāmbavant personally witnessed every deed he attributes to his addressee.

The selected Viṣṇu Purāṇa passage has a different emphasis: [4.13.19–21](https://press-files.anu.edu.au/downloads/press/n8264/html/book04.xhtml?page=9&referer=) moves from defeat to acknowledgment of Kṛṣṇa's connection to Nārāyaṇa, healing and the presentation of Jāmbavatī. The explicit Laṅkā recollection discussed here belongs to the Bhāgavata passage. These selected tellings should not be flattened into a single speech.

## 4. The jewel changes meaning as it moves

In [Viṣṇu Purāṇa 4.13.7–23](https://press-files.anu.edu.au/downloads/press/n8264/html/book04.xhtml?page=9&referer=), the jewel moves from a divine gift and coveted possession into a child's plaything, then becomes part of the resolution of suspicion against Kṛṣṇa. Its path brings a household encounter into a public dispute.

**Reading:** Jāmbavant is a hinge between domestic, political and theological scenes. These categories describe our reading, not an explicit classification by the text. The graph's Satrājita conflict captures only shared adjacency to Kṛṣṇa; it misses the jewel's changing role and the sequence of accusation, encounter and return.

## What survives if we keep the dossiers separate?

The Rāmāyaṇa recollection of Trivikrama and the Bhāgavata address invoking Laṅkā remain within their respective passages even without merging Jāmbavant records. That gives the continuity reading textual support beyond name matching.

By contrast, his global centrality, the exact MWIS shortlist and its 0.74% forced-in cost depend on the aligned graph. Our [earlier identity sensitivity experiment](README.md#what-the-deeper-graph-test-changes) showed how strongly prominence changes when the dossiers are split. The current path audit does not establish that every alignment is correct.

## Resulting narrative hypothesis

**Jāmbavant can be read as a character through whom earlier divine deeds become relevant to a present crisis—but that recognition must sometimes be reached through conflict.** The strongest new contrast is between his experience and his initial misrecognition, not simply the length of his life.

A useful next comparative question is how different tellings stage this transition: what initiates the conflict, what prompts recognition, which earlier deeds are invoked, and what relationship follows? Establishing chronology or influence between tellings would require evidence beyond this graph and translation review.
