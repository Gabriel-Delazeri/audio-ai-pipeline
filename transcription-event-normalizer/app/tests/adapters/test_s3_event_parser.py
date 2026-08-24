from datetime import datetime, timezone

import pytest

from adapters.s3_event_parser import S3EventParser


@pytest.fixture
def parser():
    return S3EventParser()


@pytest.fixture
def s3_event():
    return {
        "Records": [
            {
                "eventTime": "2026-08-24T00:19:23.334Z",
                "s3": {
                    "bucket": {"name": "audio"},
                    "object": {"key": "test.m4a", "size": 7758658},
                },
            }
        ]
    }


class TestS3EventParser:
    def test_parses_bucket(self, parser, s3_event):
        result = parser.parse(s3_event)
        assert result.audio_file.bucket == "audio"

    def test_parses_key(self, parser, s3_event):
        result = parser.parse(s3_event)
        assert result.audio_file.key == "test.m4a"

    def test_parses_size(self, parser, s3_event):
        result = parser.parse(s3_event)
        assert result.audio_file.size == 7758658

    def test_parses_event_time(self, parser, s3_event):
        result = parser.parse(s3_event)
        expected = datetime(2026, 8, 24, 0, 19, 23, 334000, tzinfo=timezone.utc)
        assert result.requested_at == expected

    def test_url_decodes_key_with_spaces(self, parser, s3_event):
        s3_event["Records"][0]["s3"]["object"]["key"] = "bending%20hectic.m4a"
        result = parser.parse(s3_event)
        assert result.audio_file.key == "bending hectic.m4a"

    def test_url_decodes_key_with_special_chars(self, parser, s3_event):
        s3_event["Records"][0]["s3"]["object"]["key"] = "audio%2Fsubfolder%2Ffile.mp3"
        result = parser.parse(s3_event)
        assert result.audio_file.key == "audio/subfolder/file.mp3"

    def test_raises_on_missing_records(self, parser):
        with pytest.raises(KeyError):
            parser.parse({})

    def test_raises_on_empty_records(self, parser):
        with pytest.raises(IndexError):
            parser.parse({"Records": []})

    def test_raises_on_missing_s3_field(self, parser):
        with pytest.raises(KeyError):
            parser.parse({"Records": [{"eventTime": "2026-08-24T00:00:00Z"}]})
