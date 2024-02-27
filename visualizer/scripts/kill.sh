#!/bin/bash
lsof -P | grep ':8050' | awk '{print $2}' | xargs kill -9