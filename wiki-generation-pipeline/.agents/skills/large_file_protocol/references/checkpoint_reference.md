# SECTION 13 — Checkpoint Reference

All checkpoints must be completed in the order listed. No checkpoint may be bypassed.

| Checkpoint | Phase | Verification method |
|---|---|---|
| Configuration Preamble recorded | Pre-Phase 0 | Check `log.md` for preamble entry |
| Exact total line count recorded | Phase 0 | Check `log.md` Phase 0 entry |
| Reading plan written | Phase 0 | Check `log.md` for chunk size and count |
| Source format identified | Phase 0 | Check `log.md` Phase 0 entry |
| Phase 0 Gate passed | Phase 0 | All Phase 0 Gate checkboxes confirmed |
| Every chunk read | Phase 1 | `log.md` lists every chunk as COMPLETE |
| Spine complete | Phase 1 | `spine.md` has entry for every chunk |
| Line count arithmetically reconciled | Phase 1 | Sum of chunk ranges = total line count |
| Oracle-DAG decision recorded | Phase 1 | `log.md` Oracle-DAG decision entry present |
| Phase 1 Gate passed | Phase 1 | All Phase 1 Gate checkboxes confirmed |
| *(If Oracle-DAG)* Dependency map created | Oracle-DAG | `dependency_map.json` exists on disk |
| *(If Oracle-DAG)* DAG generated and recorded | Oracle-DAG | `log.md` DAG entry present |
| *(If Oracle-DAG)* Subagents use boundary-enforcing prompts | Oracle-DAG | Prompts match Section 5 Step 3 pattern |
| *(If Oracle-DAG)* Merge complete in dependency order | Oracle-DAG | `log.md` merge entry present |
| All chunks processed for extraction | Phase 2 | Every Phase 1 chunk has Phase 2 disposition |
| Topic pages written | Phase 2 | `topics/` directory populated |
| All contradictions logged | Phase 2 | All flagged items in `contradictions.md` as PENDING |
| `index.md` current | Phase 2 | Index reflects all topic pages |
| Phase 2 Gate passed | Phase 2 | All Phase 2 Gate checkboxes confirmed |
| All cross-references added | Phase 3 | No orphan pages; all links verified |
| All contradictions resolved or escalated | Phase 3 | No PENDING entries in `contradictions.md` |
| Distribution check passed | Phase 3 | No topic page exceeds 40% of total wiki content |
| Gap audit complete | Phase 3 | Sparse coverage documented; misses corrected |
| Lint check passed | Phase 3 | All lint issues resolved or noted |
| Phase 3 Gate passed | Phase 3 | All Phase 3 Gate checkboxes confirmed |
| Output map complete | Phase 4 | `output_map.md` covers all output sections |
| All wiki pages have mapping status | Phase 4 | Every page mapped or logged as not relevant |
| Master summary written | Phase 4 | `master_summary.md` exists and is complete |
| Phase 4 Gate passed | Phase 4 | All Phase 4 Gate checkboxes confirmed |

---

## Scraping-Phase Checkpoints

These checkpoints apply when web scraping is used to source content for the wiki.

| Checkpoint | Phase | Verification method |
|---|---|---|
| Scraper executed successfully for all URLs | Pre-LFP | `scraped_content/manifest.json` lists all target URLs |
| `scraped_content/` populated with expected files | Pre-LFP | Count files in `scraped_content/` matches manifest entry count |
| Deduplication verified | Pre-LFP | Re-running scraper with same URLs produces all `[SKIP]` |
| Each scraped file has valid YAML frontmatter | Phase 0 | Every `.md` file in `scraped_content/` starts with `---` and contains `url:` field |
| Scraper extraction quality flagged | Phase 0 | Files with `[SCRAPER-QUALITY-LOW]` in spine are noted in `log.md` |
| Domain diversity assessed | Phase 0 | Unique domains listed in Configuration Preamble; bias noted if >40% single domain |
| All scraped content processed through Phase 2 | Phase 2 | Every scraped file has a disposition in a topic page or is logged as off-topic/redundant |
| No orphan scraped files | Phase 4 | Every file in `scraped_content/` is referenced in `log.md` at least once |
