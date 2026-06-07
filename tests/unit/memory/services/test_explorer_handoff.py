"""Tests for Explorer Builder handoff artifact generation."""

from memory.services.explorer_handoff import write_builder_handoff_artifacts
from memory.services.explorer_story import (
    ExplorerAttractor,
    ExplorerExperimentProposal,
    ExplorerStory,
)


def test_write_builder_handoff_artifacts_creates_transfer_document_set(tmp_path):
    story = ExplorerStory(
        journey="explorer-mode",
        current_exploratory_story="Explorer has clarified a Builder boundary.",
        narrative_field_summary="A handoff artifact should transfer discovery.",
        last_story_card="Story thickened around transfer docs.",
        attractors=(ExplorerAttractor(label="External validation"),),
        experiment_proposal=ExplorerExperimentProposal(title="Validate in Pi"),
    )

    handoff = write_builder_handoff_artifacts(
        tmp_path,
        story,
        title="Build Explorer persistence",
        summary="The exploration clarified the Builder boundary.",
        editorial_synthesis="The exploration continuously thickened around transfer docs.",
    )

    artifact_dir = tmp_path / "docs" / "project" / "explorations" / "build-explorer-persistence"
    assert handoff.artifact_dir == str(artifact_dir)
    index = artifact_dir / "index.md"
    exploratory_story = artifact_dir / "exploratory-story.md"
    handoff_info = artifact_dir / "handoff-info.md"
    product_design = artifact_dir / "product-design-proposal.md"
    assert index.is_file()
    assert exploratory_story.is_file()
    assert handoff_info.is_file()
    assert product_design.is_file()
    assert "The exploration continuously thickened" in index.read_text()
    assert "Explorer has clarified" in exploratory_story.read_text()
    assert "Continuous Thickening Narrative" in exploratory_story.read_text()
    assert "What Builder Should Not Assume" not in handoff_info.read_text()
    assert "Non-Assumptions" in handoff_info.read_text()
    assert "Product Design Proposal" in product_design.read_text()
    assert "does not define implementation architecture" in product_design.read_text()


def test_write_builder_handoff_artifacts_avoids_existing_directory(tmp_path):
    story = ExplorerStory(journey="explorer-mode")
    existing = tmp_path / "docs" / "project" / "explorations" / "build-explorer-persistence"
    existing.mkdir(parents=True)

    handoff = write_builder_handoff_artifacts(
        tmp_path,
        story,
        title="Build Explorer persistence",
    )

    assert handoff.artifact_dir.endswith("build-explorer-persistence-2")
